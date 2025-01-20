import asyncio
import websockets
import json
import os

PORT = int(os.environ.get("PORT", 5000))  # Obține portul dinamic de pe Render

# Stocăm dispozitivele conectate
connected_devices = {}

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

async def http_handler(websocket, path):
    """
    Handle incoming connections, both HTTP and WebSocket.
    """
    if "Upgrade" in websocket.request_headers and websocket.request_headers["Upgrade"].lower() == "websocket":
        # Este o conexiune WebSocket validă
        await handle_client(websocket, path)
    else:
        # Este o solicitare HTTP normală
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 13\r\n"
            "\r\n"
            "Hello, World!"
        )
        await websocket.send(response)
        await websocket.close()

# Pornim serverul WebSocket/HTTP
async def main():
    async with websockets.serve(http_handler, "0.0.0.0", PORT):
        print(f"Server is running on ws://0.0.0.0:{PORT}")
        await asyncio.Future()  # Rulează serverul la nesfârșit

asyncio.run(main())
