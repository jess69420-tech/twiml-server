from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Dial

app = Flask(__name__)

@app.route("/voice", methods=["GET", "POST"])
def voice():
    number_to_dial = request.values.get("To")
    response = VoiceResponse()

    if number_to_dial:
        dial = Dial()
        dial.number(number_to_dial)
        response.append(dial)
    else:
        response.say("No number specified.")

    return Response(str(response), mimetype="text/xml")
