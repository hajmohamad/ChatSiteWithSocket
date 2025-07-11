import asyncio
import websockets
import socket

clients = {}
messages = []
async def handle_client(websocket, path):
    username = await websocket.recv()
    clients[websocket] = username
    welcome_message = f"{username} به چت خوش آمدید!"
    print(welcome_message)
    await websocket.send(welcome_message)
    for mes in messages:
     await   websocket.send(mes)

    await broadcast(welcome_message,websocket)
    try:
        while True:
            message = await websocket.recv()
            print(f"[{username}]: {message}")
            if message.startswith('@'):  
                parts = message.split(' ', 1) 
                target_name = parts[0][1:]  
                private_message = f"[پیام خصوصی از {username}]: {parts[1]}" if len(parts) > 1 else ""
                await send_private_message(target_name, private_message)
            else:  
                messages.append(f"[{username}]: {message}")
                await broadcast(f"[{username}]: {message}",websocket)

    except websockets.exceptions.ConnectionClosed:
        print(f"{username} قطع شده است.")
    finally:
        await broadcast(f"{username} از چت خارج شد.",websocket)
        del clients[websocket]


async def broadcast(message,websocket):
    for client in clients:
        if client!=websocket:
         await client.send(message)

async def send_private_message(target_name, message):
    target_client = None
    for client, username in clients.items():
        if username == target_name:
            target_client = client
            break
    if target_client:
        await target_client.send(message)

import socket

def get_local_ip():
    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)  
        s.connect(('10.254.254.254', 1)) 
        local_ip = s.getsockname()[0]  
    except Exception:
        local_ip = '127.0.0.1' 
    finally:
        s.close()  
    return local_ip


ip_address = get_local_ip()
print(f"Server is running on IP: {ip_address}")
start_server = websockets.serve(handle_client, ip_address, 21345)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
