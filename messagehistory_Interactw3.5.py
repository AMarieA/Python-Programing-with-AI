from openai import OpenAI

client = OpenAI()

message = ""
messages = []

system_msg = input("What type of assistant would you like to create?\n") 
messages.append({"role": "system", "content": system_msg})

print("\nYour helper is ready!")
print("Type a question that relates to the assistance expertise and I will answer. To quit, type stop\n")

while message != "stop":
    message = input("You:  ")
    if message == "stop":
        break
    else:
        messages.append({"role": "system", "content": message})
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        print("\nHelper: " + reply + "\n")

print("Helper signed off")