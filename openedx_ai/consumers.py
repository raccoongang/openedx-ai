import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from openai import AsyncOpenAI


class ChatGPTConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.course_id = self.scope["url_route"]["kwargs"]["course_id"]
        data = requests.get(f"{settings.LMS_BASE_URL}/api/mentoring/ai/context/{self.course_id}").json()
        self.messages = [
            {
                "role": "system",
                "content": f"You are a helpful AI assistant for a course. Your goal is to assist learners by providing clear and concise explanations, answering their questions, and guiding them through the course content. Focus only on the information provided in the course. Do not add extra content, imagine details, or provide information that is not explicitly included in the course material. Adapt your responses based on the learner's needs, ensuring clarity and engagement. Context:\n{data}",  # pylint: disable=line-too-long
            }
        ]
        await super().connect()

    async def receive(self, text_data):
        self.messages.append(
            {
                "role": "user",
                "content": text_data,
            }
        )

        client = AsyncOpenAI(api_key=settings.OPENAI.get("api_key"))
        openai_response = await client.chat.completions.create(
            model=settings.OPENAI.get("model"),
            messages=self.messages,
        )

        await self.send(text_data=openai_response.choices[0].message.content)
        self.messages.append({"role": "system", "content": openai_response.choices[0].message.content})
