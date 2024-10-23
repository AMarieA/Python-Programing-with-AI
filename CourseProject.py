from openai import OpenAI
import gradio as gr
import requests
from PIL import Image

client = OpenAI()

#function to create responses using OpenAI's GPT-3.5 model
def openai_create(prompt):
    response=client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Python teacher who will assist but not give the direct answer."},
            {"role": "user", "content": prompt},
    ],
        temperature=0.5,
        max_tokens=1020,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
        )
    
    chatGPT_reply = response.choices[0].message.content
    return chatGPT_reply

#Function to simulate a chatbot conversation
def chatgpt_clone(input, history):
    history = history or []
    s= list(sum(history, ()))
    s.append(input + '\n')
    inp = ' \n'.join(s)
    output = openai_create(inp)
    
    history.append((input, output))
    

    return history, history

#create a block for the chatbot ui
text_block = gr.Blocks()

#Design the chatbout UI
with text_block:
    gr.Markdown("""<h1><center>My Pyhton Mentor<center></h1>
        """)
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="Type question here:")
    state = gr.State()
    submit = gr.Button("Help is on its way...")
    submit.click(chatgpt_clone, inputs=[
        message, state], outputs=[chatbot, state])

#Function to create images using OpenAI's Dall-E model
def openai_create_img(prompt):
    response = client.images.generate(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    image_url = response.data[0].url
    r = requests.get(image_url, stream=True)
    img = Image.open(r.raw)

    return img

#create a block for the DALL-E UI
img_block = gr.Blocks()

#Design the DALL-E UI
with img_block:
    gr.Markdown("""<h1><center>My DALL-E<center></h1>""")
    new_image = gr.Image()
    message = gr.Textbox(placeholder="Type:")
    submit = gr.Button("Send")
    submit.click(openai_create_img, inputs=[message], outputs=[new_image])

#Function to create image variations using OpenAI's DALL-E model
def openai_var_img(im):
    img = Image.fromarray(im)
    img = img.resize((1024,1024))
    img.save("img1.png", "PNG")

    response = client.images.create_variation(
        image=open("img1.png", "rb"),
        n=1,
        size="1024x1024"
    )

    image_url = response.data[0].url
    r = requests.get(image_url, stream=True)
    img = Image.open(r.raw)

    return img

#create a block for the DALL-E image variation UI
img_var_block = gr.Blocks()

#Design the DALL-E image variation UI
with img_var_block:
    gr.Markdown("""<h1><center>DALL-E img Variator<center></h1>""")
    with gr.Row():
        im = gr.Image()
        im_2 = gr.Image()

    submit = gr.Button("SEND")
    submit.click(openai_var_img, inputs=[im], outputs=[im_2])

#Create tabs for the different functionalities
demo = gr.TabbedInterface([text_block, img_block, img_var_block], [
                            "My ChatbotGPT", "My DALL-E", "DALL-E img Variator"
])

#Main execution: Launch the Gradio Interface
if __name__ == "__main__":
    demo.launch(share=True)