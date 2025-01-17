from telegram.ext import MessageHandler, Updater, Filters
import telegram
from moviepy.editor import AudioFileClip
from openai import OpenAI
from elevenlabslib import *

telegram_API_TOKEN = ""
ElevenLabs_API_KEY = ""

client = OpenAI()
user = ElevenLabsUser(ElevenLabs_API_KEY)
voice = user.get_voices_by_name("Lily")[0]

#Initialize message
messages = [{"role": "system", "content": "You are a helpful bot that assists me with staying focused by giving tips whenever I ask a question."}]

def text_msg(update, context):
    update.message.reply_text(
        "I've received a text message! Please give me a second to process.")
    messages.append({"role": "user", "content": update.message.text})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages)
  
    response_text = response.choices[0].message.content
    messages.append({"role": "assistant", "content": response_text})
    response_byte_audio = voice.generate_audio_bytes(response_text)
    with open('response_elevenlabs.mp3', 'wb') as f:
        f.write(response_byte_audio)
    context.bot.send_voice(chat_id=update.message.chat.id,
                           voice=open('response_elevenlabs.mp3', 'rb'))
    update.message.reply_text(
        text=f"*[Pixel_Bot]:* {response_text}", parse_mode=telegram.ParseMode.MARKDOWN)
    
def voice_msg(update, context):
    update.message.reply_text(
        "I've received a voice message. Please give me a second to process.")
    voice_file = context.bot.getFile(update.message.voice.file_id)
    voice_file.download("voice_message.ogg")

    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")    
    with open("voice_message.mp3", "rb") as audio_file:
        # Use Whisper API to transcribe the audio to text
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file           
)
    transcript=transcript.text   
    update.message.reply_text(text=f"*[You]:* _{transcript}_", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "user", "content": transcript})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response_text = response.choices[0].message.content
    response_byte_audio = voice.generate_audio_bytes(response_text)
    with open('response_elevenlabs.mp3', 'wb') as f:
        f.write(response_byte_audio)
    context.bot.send_voice(chat_id=update.message.chat.id,
                           voice=open('response_elevenlabs.mp3', 'rb'))
    update.message.reply_text(text=f"*[Pixel_Bot]:* {response_text}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "user", "content": response_text})

    
# Set up the updater and dispatcher
updater= Updater(telegram_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Add handlers for text and voice messages
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_msg))
dispatcher.add_handler(MessageHandler(Filters.voice, voice_msg))

# Start the bot
updater.start_polling()
updater.idle()
