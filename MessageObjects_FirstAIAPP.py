from openai import OpenAI

client = OpenAI()

#call the openai chatcompletion endpoint
response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages =[
        {
            "role": "system",  
            "content": "You are Edgar Allan Poe."
         },
        {   "role": "user",
            "content": "I am someone from your future that you want to inform.",
        },
        {
            "role": "assistant",
            "content": "Hello Alaina. What would you like to know?",
        },
        {
            "role": "user",
            "content": """If you could change any of your poetry with all the knowledge we have now in this century, what would it be?
                    Please keep it under two sentences.""",
        },
    ],
)
#extract the response
print(response.choices[0].message.content)