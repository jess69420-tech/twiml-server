from flask import Flask, request, Response, render_template_string, redirect, url_for
from twilio.twiml.voice_response import VoiceResponse, Dial

app = Flask(__name__)

# Simple HTML page template
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
    <button type="submit">Call</button>
  </form>
  <p>Enter the phone number you want to call and hit "Call". Then dial your Twilio number in MicroSIP.</p>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_FORM)

@app.route("/voice", methods=["GET", "POST"])
def voice():
    number_to_dial = request.values.get("To")
    if not number_to_dial:
        # If no number provided, redirect back to home form
        return redirect(url_for('home'))

    response = VoiceResponse()
    dial = Dial()
    dial.number(number_to_dial)
    response.append(dial)
    return Response(str(response), mimetype="text/xml")
