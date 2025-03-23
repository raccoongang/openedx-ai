from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from openai import AsyncOpenAI


class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data="WebSocket connected!")

    async def receive(self, text_data):
        await self.send(text_data=text_data)

    async def disconnect(self, close_code):
        print("WebSocket disconnected:", close_code)


class ChatGPTConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.course_id = self.scope["url_route"]["kwargs"]["course_id"]
        # TODO: Provide openedx course context
        self.messages = [
            {
                "role": "system",
                "content": f"You are a helpful AI assistant for course {self.course_id}. Respond concisely and clearly.",
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
