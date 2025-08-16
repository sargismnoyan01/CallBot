import json
from channels.generic.websocket import AsyncWebsocketConsumer
from deepgram import Deepgram
import os
import base64

DG_API_KEY = "ՔՈ_DEEPGRAM_API_KEY"

class AudioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.dg_client = Deepgram(DG_API_KEY)
        self.buffer = b""

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            self.buffer += bytes_data

        if text_data:
            message = json.loads(text_data)
            if message.get("type") == "stop":
                transcript = await self.transcribe_audio(self.buffer)
                await self.send(json.dumps({"text": transcript}))
                self.buffer = b""

    async def transcribe_audio(self, audio_data):
        source = {"buffer": audio_data, "mimetype": "audio/webm"}
        response = await self.dg_client.transcription.prerecorded(
            source, {"punctuate": True}
        )
        return response["results"]["channels"][0]["alternatives"][0]["transcript"]