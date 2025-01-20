import asyncio
import websockets
import json
import os

# Obține portul dinamic din variabila de mediu
PORT = int(os.environ.get("PORT", 5000))

# Stocăm dispozitivele conectate
connected_devices = {}
connected_clients = set()

async def handle_client(websocket, path):
    """
    Gestionează conexiunile clienților (Android sau Desktop).
    """
    print("New connection established!")
    try:
        async for message in websocket:
            data = json.loads(message)

            # Gestionăm tipul mesajului
            message_type = data.get("type")
            if message_type == "register":
                # Înregistrăm dispozitivul Android
                device_id = data.get("device_id")
                connected_devices[device_id] = websocket
                print(f"Device {device_id} registered.")

            elif message_type == "command":
                # Trimiterea unei comenzi de la desktop către Android
                device_id = data.get("device_id")
                command = data.get("command")
                if device_id in connected_devices
