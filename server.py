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
                if device_id in connected_devices:
                    device_websocket = connected_devices[device_id]
                    await device_websocket.send(json.dumps({"command": command}))
                    print(f"Command '{command}' sent to {device_id}.")
                else:
                    print(f"Device {device_id} not found.")

            elif message_type == "status":
                # Actualizare stare de la Android
                device_id = data.get("device_id")
                status = data.get("status")
                print(f"Device {device_id} status: {status}")

            else:
                print("Unknown message type received.")

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed.")
    finally:
        # Eliminăm conexiunea la deconectare
        if websocket in connected_devices.values():
            for device_id, device_ws in list(connected_devices.items()):
                if device_ws == websocket:
                    del connected_devices[device_id]
                    print(f"Device {device_id} disconnected.")
        connected_clients.discard(websocket)

# Pornim serverul WebSocket
async def main():
    async with websockets.serve(handle_client, "0.0.0.0", PORT):
        print(f"Server is running on ws://0.0.0.0:{PORT}")
        await asyncio.Future()  # Rulează la nesfârșit

asyncio.run(main())
