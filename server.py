import asyncio
import websockets
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import os

PORT = int(os.environ.get("PORT", 5000))  # Obține portul dinamic de pe Render
connected_devices = {}  # Dispozitivele conectate

class HealthCheckHandler(BaseHTTPRequestHandler):
    """
    Un handler HTTP simplu pentru gestionarea solicitărilor HEAD/GET.
    """
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, World!")

def start_http_server():
    """
    Pornește un server HTTP pentru gestionarea solicitărilor de sănătate.
    """
    server = HTTPServer(("0.0.0.0", PORT), HealthCheckHandler)
    print(f"HTTP server is running on http://0.0.0.0:{PORT}")
    server.serve_forever()

async def handle_client(websocket, path):
    """
    Gestionează conexiunile WebSocket.
    """
    try:
        async for message in websocket:
            data = json.loads(message)
            message_type = data.get("type")

            if message_type == "register":
                device_id = data.get("device_id")
                connected_devices[device_id] = websocket
                print(f"Device {device_id} registered.")

            elif message_type == "command":
                device_id = data.get("device_id")
                command = data.get("command")
                if device_id in connected_devices:
                    device_websocket = connected_devices[device_id]
                    await device_websocket.send(json.dumps({"command": command}))
                    print(f"Command '{command}' sent to {device_id}.")
                else:
                    print(f"Device {device_id} not found.")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        # Curățare la deconectare
        for device_id, ws in list(connected_devices.items()):
            if ws == websocket:
                del connected_devices[device_id]
                print(f"Device {device_id} disconnected.")

async def start_websocket_server():
    """
    Pornește serverul WebSocket.
    """
    async with websockets.serve(handle_client, "0.0.0.0", PORT):
        print(f"WebSocket server is running on ws://0.0.0.0:{PORT}")
        await asyncio.Future()  # Rulează la nesfârșit

if __name__ == "__main__":
    # Pornește serverul HTTP într-un thread separat
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()

    # Pornește serverul WebSocket
    asyncio.run(start_websocket_server())
