from ollama import chat
from ollama import ChatResponse

system_prompt = (
    "You are a productivity assistant. Ask the user for missing details only if needed. "
    "Then produce: (1) prioritized task list, (2) time-blocked schedule, (3) next actions."
)

user_tasks = input("Enter your tasks for today (you can paste a list):\n> ")

response: ChatResponse = chat(
    model="deepseek-r1:1.5b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_tasks},
    ],
)

print(response.message.content)

