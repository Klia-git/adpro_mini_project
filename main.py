from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='deepseek-r1:1.5b', messages=[
  {
      'role': 'system',
      'content': 'You are a productivity assistant. Help the user organize their day by structuring tasks into a clear plan with priorities and time blocks.'
    },
    {
      'role': 'user',
      'content': 'I have to study machine learning, answer emails, go to the gym, and buy groceries. Help me structure my day.'
    }
  ]
)
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)
