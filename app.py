from flask import Flask, request, Response, render_template_string, redirect, url_for
from twilio.twiml.voice_response import VoiceResponse, Dial

app = Flask(__name__)

# Store last number globally (in memory)
last_number_to_dial = None

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
  <title>Call Dialer</title>
</head>
<body>
  <h1>Call Dialer</h1>
  <form method="get" action="/voice">
    <label for="To">Phone Number to Call:</label>
    <input type="tel" id="To" name="To" placeholder="+1234567890" required>
    <button type="submit">Set Number</button>
  </form>
  <p>Enter the phone number you want to call and hit "Set Number". Then dial your Twilio number in MicroSIP.</p>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_FORM)

@app.route("/voice", methods=["GET", "POST"])
def voice():
    global last_number_to_dial

    number_to_dial = request.values.get("To")

    if number_to_dial:
        # Update last_number_to_dial when URL param provided
        last_number_to_dial = number_to_dial
        # If accessed from browser, show XML
        response = VoiceResponse()
        dial = Dial()
        dial.number(number_to_dial)
        response.append(dial)
        return Response(str(response), mimetype="text/xml")

    # If no To param, use last saved number
    if last_number_to_dial:
        response = VoiceResponse()
        dial = Dial()
        dial.number(last_number_to_dial)
        response.append(dial)
        return Response(str(response), mimetype="text/xml")

    # No number set yet, redirect to form
    return redirect(url_for('home'))
