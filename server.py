from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_client_data():
    data = request.data.decode('utf-8')
    print(f"Received data from client: {data}")
    return "Data received", 200

@app.route('/command', methods=['GET'])
def send_command():
    commands = [
        {"action": "show_message", "message": "This is a server message!"},
        {"action": "get_device_info"},
        {"action": "get_installed_apps"},
    ]
    return jsonify(commands)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
