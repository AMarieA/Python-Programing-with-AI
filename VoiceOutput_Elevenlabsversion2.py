from telegram.ext import Application, MessageHandler, filters
from telegram.constants import ParseMode
from moviepy.editor import AudioFileClip
from openai import OpenAI
from elevenlabslib import *

client = OpenAI()

telegram_API_TOKEN = "7359144680:AAFrv8mGk2tz6QWTwn-4E7Pa4T8fGqpudWk"
ElevenLabs_API_KEY = "sk_4f636dc58438e85842da12e1b5626fa4045021cf5d10b215"

user= ElevenLabsUser(ElevenLabs_API_KEY)
#List due to multiple voices can have same name
voice=user.get_voices_by_name("Lily")[0]

#Initialize message
messages = [{"role": "system",
            "content": "You are a helpful assistant that starts it's response by referring to the user as its master."}]

#text message FUNCTION
async def text_msg(update, context):
    await update.message.reply_text(
        "I've received a text message! Please give me a second to respond."
    )
    messages.append({"role": "user", "content": update.message.text})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    #extractions
    response_text = response.choices[0].message.content

    #Append reply 
    messages.append({"role": "assistant", "content": response_text})

    response_byte_audio = voice.generate_audio_bytes(response_text)

    #Send voice response
    with open('response_elevenlabs.mp3', 'wb') as f:
        f.write(response_byte_audio)
    
    context.bot.send_voice(chat_id=update.message.chat.id,
                           voice=open('response_elevenlabs.mp3', 'rb'))
    
    #Then send the text response
    await update.message.reply_text(
        text=f"*[Pixel_Bot]:* {response_text}", parse_mode=ParseMode.MARKDOWN)
    
    

#Voice Message Function to handle voice msgs
async def voice_msg(update, context):
    await update.message.reply_text("I've received a voice message. Please give me a second to respond.")
    
    # Download and convert voice message
    voice_file = await context.bot.getFile(update.message.voice.file_id)
    await voice_file.download_to_drive("voice_message.ogg")
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")

    # Transcribe audio to text
    with open("voice_message.mp3", "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    transcript_text = str(transcript)
    await update.message.reply_text(text=f"*[You]:* _{transcript_text}_", parse_mode=ParseMode.MARKDOWN)
    
    messages.append({"role": "user", "content": transcript_text})
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    response_text = response.choices[0].message.content
    messages.append({"role": "assistant", "content": response_text})

    response_byte_audio = voice.generate_audio_bytes(response_text)
    with open('response_elevenlabs.mp3', 'wb') as f:
        f.write(response_byte_audio)

    context.bot.send_voice(chat_id=update.message.chat.id, voice=open('response_elevenlabs.mp3', 'rb'))
    await update.message.reply_text(text=f"*[Pixel_Bot]:* {response_text}", parse_mode=ParseMode.MARKDOWN)

    

#Telegram Bot Setup with newest version
handler = Application.builder().token(telegram_API_TOKEN).build()

handler.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), text_msg))
handler.add_handler(MessageHandler(filters.VOICE, voice_msg))

handler.run_polling()  # Start the Bot

handler.idle() #Run bot until the user presses Ctrl-C
    