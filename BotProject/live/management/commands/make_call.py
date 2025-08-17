# myapp/management/commands/make_call.py

from django.core.management.base import BaseCommand
from twilio.rest import Client
import os

class Command(BaseCommand):
    help = 'Make an outgoing call via Twilio and stream user audio to WebSocket'

    def handle(self, *args, **kwargs):
        # Twilio հաշվի տվյալներ
        account_sid = os.getenv('TWILIO_SID')
        auth_token = os.getenv('TWILIO_auth_token')
        client = Client(account_sid, auth_token)

        # Outgoing call
        call = client.calls.create(
            twiml = '''
            <Response>
                <Start>
                    <Stream url="wss://yourdomain.com/ws/twilio/stream/"/>
                </Start>
                <Say voice="alice" language="en-US">
                    Hello, we would like to introduce our services.
                </Say>
            </Response>
            ''',

            to=os.getenv('TWILIO_TO'),      # <-- Ով ենք զանգում (հաճախորդի համար)
            from_=os.getenv('TWILIO_FROM')    # <-- Twilio համար
        )

        self.stdout.write(f"Outgoing call initiated, Call SID: {call.sid}")
