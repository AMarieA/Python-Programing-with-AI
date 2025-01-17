from openai import OpenAI
import gradio

client = OpenAI()

messages = [{"role": "system", "content": "You are a a dog trainer who dedicates time into the German Shepard breed."}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

demo = gradio.Interface(fn=CustomChatGPT, inputs="text",
                        outputs="text", title="Dog Trainer")

demo.launch(share=True)