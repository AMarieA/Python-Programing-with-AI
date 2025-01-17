from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode

from moviepy.editor import AudioFileClip

from openai import OpenAI

client = OpenAI()

telegram_API_TOKEN = ""

messages = [{"role": "system",
            "content": "You are a helpful telegram bot who is always conside and polite in its answers."}]

#define a function called 'text message' to hangle text messages.
async def text_msg(update, context):
    #Append the user's message to the 'messages' list
    messages.append({"role": "user", "content": update.message.text})

    #send the 'messages' list to the GPT-3.5 Turbo model and get a response.
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=messages
    )

    #extract the reply from the ChatGPT model's response
    ChatGPT_reply = response.choices[0].message.content

    #send the ChatGPT reply back to the user via Telegram
    await update.message.reply_text(
        text=f"*[Pixel_Bot]:* {ChatGPT_reply}", parse_mode=ParseMode.MARKDOWN)
    
    #Append the assistant's reply to the "messages" list for future interactions
    messages.append({"role": "assistant", "content": ChatGPT_reply})

#####################################################################################################

async def voice_message(update, context):
    #Notify the user that the voice message is being processed
    await update.message.reply_text(
        "I've received a voice message! Please give me a second to response :)")
    
    bot=context.bot

    #Download the voice message from Telegram
    voice_file = await bot.getFile(update.message.voice.file_id)
    await voice_file.download_to_drive("voice_message.ogg")

    #convert the voice message from OGG to MP3 format
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")

    # Open the MP3 audio file
    with open("voice_message.mp3", "rb") as audio_file:
        # Use Whisper API to transcribe the audio to text
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file           
)
     # Extract the transcribed text from the response    
    transcript_text = transcript.text 

    #Send the transcribed text back to the user for confirmation
    await update.message.reply_text(
        text=f"*[You]:* _{transcript_text}_", parse_mode=ParseMode.MARKDOWN)

    #Send the transcribed text to the 'messages' list
    messages.append({"role": "user", "content": transcript_text})

    #get reply from ChatGPT
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response.choices[0].message.content

    #Send ChatGPT's reply back the the user
    await update.message.reply_text(
        text=f"*[Pixel_Bot]:* {ChatGPT_reply}", parse_mode=ParseMode.MARKDOWN)
    
    #Append the ChatGPT reply to the "messages" list
    messages.append({"role": "assistant", "content": ChatGPT_reply})   


#Telegram Bot Setup with newest version
app = Application.builder().token(telegram_API_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), text_msg))
app.add_handler(MessageHandler(filters.VOICE, voice_message))

app.run_polling()  # Start the Bot

app.idle() #Run bot until the user presses Ctrl-C


##NOTES
#The await keyword is used in asynchronous programming to pause the execution of a function until a certain task completes. 
