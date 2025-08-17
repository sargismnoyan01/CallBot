from django.shortcuts import render
from twilio.rest import Client
from django.http import HttpResponse
import os

def make_call(request):
    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_auth_token')
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        twiml='''
        <Response>
            <Start>
                <Stream url="wss://localhost:8000/ws/twilio/stream/"/>
            </Start>
            <Say voice="alice" language="en-US">
                Hello, we would like to introduce our services.
            </Say>
        </Response>
        ''',
        to='+37494240920',   
        from_='+18157654784'    
    )

    return HttpResponse(f"Call initiated, SID: {call.sid}")
