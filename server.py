import asyncio
import websockets
import json
import os

PORT = int(os.environ.get("PORT", 5000))

connected_devices = {}

async def handle_client(websocket, path):
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
        # Cleanup
        for device_id, ws in list(connected_devices.items()):
            if ws == websocket:
                del connected_devices[device_id]
                print(f"Device {device_id} disconnected.")

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", PORT):
        print(f"WebSocket server is running on ws://0.0.0.0:{PORT}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
