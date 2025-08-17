import os
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from faster_whisper import WhisperModel
import json

class TwilioTranscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.audio_dir = os.path.join(os.getcwd(), "audio_files")
        os.makedirs(self.audio_dir, exist_ok=True)
        self.raw_path = os.path.join(self.audio_dir, "customer_audio.raw")
        self.audio_file = open(self.raw_path, "wb")

    async def disconnect(self, close_code):
        self.audio_file.close()

        model = WhisperModel("small")
        segments, info = model.transcribe(self.raw_path, language="en")

        text_path = os.path.join(self.audio_dir, "customer_text.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            for segment in segments:
                f.write(segment.text + "\n")

        print(f"Customer transcription saved as {text_path}")

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if "media" in data:
            payload = data['media']['payload']
            audio_chunk = base64.b64decode(payload)
            self.audio_file.write(audio_chunk)
