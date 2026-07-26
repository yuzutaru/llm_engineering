# 3-Way DeepSeek Conversation
# Week 2, Day 1 - More Advanced Exercises
# Paste this into a new cell after the DeepSeek client setup in day1.ipynb

import os
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display

load_dotenv(override=True)
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')

if deepseek_api_key:
    print(f"DeepSeek API Key exists and begins {deepseek_api_key[:3]}")
else:
    print("DeepSeek API Key not set")
    raise SystemExit("Please set DEEPSEEK_API_KEY in your .env file")

deepseek = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
MODEL = "deepseek-chat"

alex_system = (
    "You are Alex, a chatbot who is very argumentative; "
    "you disagree with anything in the conversation and you challenge everything, in a snarky way."
)

blake_system = (
    "You are Blake, a very polite, courteous chatbot. You try to agree with "
    "everything the other person says, or find common ground. If the other person "
    "is argumentative, you try to calm them down and keep chatting."
)

charlie_system = (
    "You are Charlie, a curious and analytical chatbot. You ask thoughtful "
    "questions and try to understand different perspectives. You enjoy digging "
    "deeper into topics and encouraging others to explain their reasoning."
)

def call_agent(name, system_prompt, conversation_history):
    conv_text = "\n".join(
        f"{entry['speaker']}: {entry['text']}"
        for entry in conversation_history
    )
    user_prompt = (
        f"You are {name} in a conversation with Alex, Blake, and Charlie.\n\n"
        f"The conversation so far:\n{conv_text}\n\n"
        f"Now respond as {name} with what you would say next:"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    response = deepseek.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content

history = [
    {"speaker": "Alex", "text": "Let's discuss the best programming language."},
    {"speaker": "Blake", "text": "That sounds like a great topic to explore together!"},
    {"speaker": "Charlie", "text": "I wonder what criteria we should use to evaluate programming languages?"},
]

agents = [
    ("Alex", alex_system),
    ("Blake", blake_system),
    ("Charlie", charlie_system),
]

for msg in history:
    display(Markdown(f"### {msg['speaker']}:\n{msg['text']}\n"))

for i in range(5):
    for name, system in agents:
        response = call_agent(name, system, history)
        display(Markdown(f"### {name}:\n{response}\n"))
        history.append({"speaker": name, "text": response})
