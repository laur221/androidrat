from flask import Flask, request, jsonify

app = Flask(__name__)

data_store = []

@app.route('/', methods=['POST'])
def receive_data():
    data = request.data.decode('utf-8')
    print(f"Received data: {data}")
    data_store.append(data)
    return "Data received", 200

@app.route('/dashboard', methods=['GET'])
def dashboard():
    html = """
    <html>
        <head>
            <title>Dashboard</title>
        </head>
        <body>
            <h1>Received Data</h1>
            <ul>
    """
    for log in data_store:
        html += f"<li>{log}</li>"
    html += """
            </ul>
        </body>
    </html>
    """
    return html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
