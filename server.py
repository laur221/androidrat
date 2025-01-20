from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_data():
    data = request.data.decode('utf-8')
    print(f"Received data: {data}")
    return "Data received", 200

@app.route('/command', methods=['GET'])
def send_command():
    commands = [
        {"action": "show_message", "message": "This is a server message!"},
        {"action": "get_device_info"},
        {"action": "get_installed_apps"},
    ]
    return jsonify(commands)
@app.route('/dashboard', methods=['GET'])
def dashboard():
    with open("data_log.txt", "r") as file:
        logs = file.readlines()
    html = "<h1>Dashboard</h1><ul>"
    for log in logs:
        html += f"<li>{log.strip()}</li>"
    html += "</ul>"
    return html


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
