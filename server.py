from flask import Flask, request, jsonify

app = Flask(__name__)

# Calea fișierului pentru stocarea datelor
DATA_LOG_FILE = "data_log.txt"

# Endpoint pentru primirea datelor
@app.route('/', methods=['POST'])
def receive_data():
    data = request.data.decode('utf-8')
    print(f"Received data: {data}")
    # Salvează datele în fișier doar dacă nu sunt goale
    if data.strip():
        with open(DATA_LOG_FILE, "a") as file:
            file.write(data + "\n")
    else:
        print("Received empty data!")  # Log pentru date goale
    return "Data received", 200

# Endpoint pentru trimiterea comenzilor către aplicația Android
@app.route('/command', methods=['GET'])
def send_command():
    commands = [
        {"action": "show_message", "message": "Hello from the server!"},
        {"action": "get_device_info"},
        {"action": "get_installed_apps"},
        {"action": "vibrate", "duration": 1000},  # Vibrație de 1 secundă
        {"action": "turn_on_flashlight"}
    ]
    return jsonify(commands)

# Endpoint pentru dashboard (vizualizarea datelor primite)
@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Verifică dacă fișierul există și citește datele
    try:
        with open(DATA_LOG_FILE, "r") as file:
            logs = file.readlines()
    except FileNotFoundError:
        logs = []  # Dacă fișierul nu există, inițializează o listă goală

    # Construiește HTML-ul pentru afișarea datelor
    html = """
    <html>
        <head>
            <title>Dashboard</title>
        </head>
        <body>
            <h1>Received Data</h1>
            <ul>
    """
    for log in logs:
        html += f"<li>{log.strip()}</li>"
    html += """
            </ul>
        </body>
    </html>
    """
    return html

# Rulează serverul
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
