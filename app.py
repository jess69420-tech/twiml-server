from flask import Flask, request, Response, render_template_string

app = Flask(__name__)

last_number = None

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Set Call Number</title>
    <script>
        function submitNumber(e) {
            e.preventDefault();
            const num = document.getElementById("number").value;
            if(!num.startsWith('+')) {
                alert("Please enter number in E.164 format starting with +");
                return;
            }
            // Open the /voice?To=NUM link in a new tab
            const url = `/voice?To=${encodeURIComponent(num)}`;
            window.open(url, '_blank');
            alert('Number set! Now call your Twilio number.');
        }
    </script>
</head>
<body>
    <h2>Set Number to Dial</h2>
    <form onsubmit="submitNumber(event)">
        <input type="text" id="number" placeholder="+1234567890" required style="width:200px;"/>
        <button type="submit">Set & Open TwiML</button>
    </form>
    <p>After setting, call your Twilio number to dial this number.</p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/voice')
def voice():
    global last_number
    to_number = request.args.get('To')
    if to_number:
        last_number = to_number.strip()

    if not last_number:
        # No number set yet, return empty TwiML
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
