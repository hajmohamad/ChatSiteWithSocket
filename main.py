import asyncio
import websockets

clients = {}
messages = []

async def handle_client(websocket):
    username = await websocket.recv()
    clients[websocket] = username

    welcome_message = f"{username} به چت خوش آمدید!"
    print(welcome_message, flush=True)

    await websocket.send(welcome_message)

    for mes in messages:
        await websocket.send(mes)

    await broadcast(welcome_message, websocket)

    try:
        while True:
            message = await websocket.recv()
            print(f"[{username}]: {message}", flush=True)

            if message.startswith('@'):
                parts = message.split(' ', 1)
                target_name = parts[0][1:]
                private_message = (
                    f"[پیام خصوصی از {username}]: {parts[1]}"
                    if len(parts) > 1 else ""
                )
                await send_private_message(target_name, private_message)
            else:
                messages.append(f"[{username}]: {message}")
                await broadcast(f"[{username}]: {message}", websocket)

    except websockets.exceptions.ConnectionClosed:
        print(f"{username} قطع شده است.", flush=True)
    finally:
        await broadcast(f"{username} از چت خارج شد.", websocket)
        del clients[websocket]


async def broadcast(message, websocket):
    for client in clients:
        if client != websocket:
            await client.send(message)


async def send_private_message(target_name, message):
    for client, username in clients.items():
        if username == target_name:
            await client.send(message)
            break


async def main():
    print("Starting WebSocket server on 0.0.0.0:21345", flush=True)
    async with websockets.serve(handle_client, "0.0.0.0", 21345):
        await asyncio.Future()  # run forever


asyncio.run(main())
