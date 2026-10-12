import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(override=True)

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

model = init_chat_model(
    "google_genai:gemini-3.6-flash",
    max_retries=10,  # Increase for unreliable networks (default: 6)
    timeout=120,  # Seconds; increase for slow connections
)

print("what mood do you wish your model to possess?")
print("press 1 for angry mode")
print("press 2 for funny mode")
print("press 3 for sad mode")
print("press 4 for romantic mode")

n = input("press the number")

mood = ""

if n == "1":
   mood = "You are in an angry mood"
elif n == "2":
     mood = "You are in an funny mood"
elif n == "3":
     mood = "You are in an sad mood"
elif n == "4":
     mood = "You are in an romantic mood"          

msg_history = [
    SystemMessage(content = mood )
]

print("press 0 to exit the conversation")

while True:

    prompt = input("enter your query : ")
    if prompt == "0":
       break;         
    
    msg_history.append( HumanMessage(content=prompt) ) 
      
    response = model.invoke(msg_history)
    msg_history.append( AIMessage(content=response.content[0]['text'] ) )
    print(response.content[0]['text'])
