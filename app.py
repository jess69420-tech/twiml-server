from flask import Flask, request, Response, render_template_string, redirect, url_for

app = Flask(__name__)

# Store last dialed number in-memory (reset on restart)
last_number = None

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Set Call Number</title>
    <script>
        function submitNumber(e) {
            e.preventDefault();
            const num = document.getElementById("number").value.trim();
            if (!num.startsWith('+')) {
                alert('Please enter the phone number in E.164 format starting with +');
                return;
            }
            // Send number to /set endpoint and then open /voice in new tab
            fetch('/set?To=' + encodeURIComponent(num))
                .then(() => {
                    window.open('/voice', '_blank');
                    alert('Number set! Now call your Twilio number.');
                });
        }
    </script>
</head>
<body>
    <h2>Set Number to Dial</h2>
    <form onsubmit="submitNumber(event)">
        <input type="text" id="number" placeholder="+1234567890" required style="width:220px;" />
        <button type="submit">Set Number & Open Call</button>
    </form>
    <p>Then call your Twilio number to dial the set number.</p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/set')
def set_number():
    global last_number
    to_number = request.args.get('To', '').strip()
    if to_number.startswith('+'):
        last_number = to_number
        return 'Number set to ' + last_number
    else:
        return 'Invalid number. Must start with +', 400

@app.route('/voice')
def voice():
    global last_number
    if not last_number:
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response></Response>"""
    else:
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Dial>{last_number}</Dial>
</Response>"""

    return Response(twiml, mimetype='text/xml')

if __name__ == '__main__':
    app.run(debug=True)
