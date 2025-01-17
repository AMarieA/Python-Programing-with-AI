from openai import OpenAI
import gradio as gr

client = OpenAI()

messages = [{"role": "system",
             "content": "You are a master negotiator. However, Your girlfriend Alaina is still always right!"}]

def CustomChatGPT(user_input, history):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    ChatGPT_reply = response.choices[0].message.content
    personalized = f"Hi Casey, the answer is: {ChatGPT_reply}"
    messages.append({"role": "assistant", "content": personalized})
    return personalized

#Customization of Web UI
demo = gr.ChatInterface(
    fn=CustomChatGPT,
    textbox=gr.Textbox(placeholder="Ask me a yes or no question", container=False, scale=3, text_align="right"
    ),
    chatbot=gr.Chatbot(),
    title="Alaina's Chatbot",   
    description="A place for simple answers", 
    theme="default",
    examples=["Hello", "Am I cool?", "Should I replace the entire A/C in the rental unit?"],
    cache_examples=False,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
    submit_btn= "Be prepared for the best answer"
    )

demo.launch(share=True)