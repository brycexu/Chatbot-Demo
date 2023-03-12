import openai
from config import certificate

openai.api_key = certificate["OpenAI"]

class ChatGPT:
    def answer(self, query):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": query}]
        )
        response = response["choices"][0]["message"]["content"][2:].replace("OpenAI", "BNY Mellon Chatbot")
        return response

