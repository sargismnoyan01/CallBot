from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

class TwilioStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.audio_buffer = b""

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            self.audio_buffer += bytes_data

            transcript, end_of_segment = await self.send_to_whisper(self.audio_buffer)
            
            if transcript:
                self.partial_transcript = transcript

            if end_of_segment:
                response = await self.send_to_gpt(self.partial_transcript)
                audio_file_url = await self.convert_text_to_speech(response)
                await self.send_json({"play_audio": audio_file_url})

    async def send_to_whisper(self, audio_buffer):
        return "Որպես օրինակ ստացված տեքստ", True

    async def send_to_gpt(self, transcript):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": transcript}],
        )
        return completion.choices[0].message["content"]

    async def convert_text_to_speech(self, text):
        return "https://yourserver.com/generated_audio.mp3"
