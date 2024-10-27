# app.py
import aiohttp
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import time
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get():
    with open("chat.html") as f:
        return HTMLResponse(f.read())

async def fetch_response(model, question, websocket):
    async with aiohttp.ClientSession() as session:
        url = "http://127.0.0.1:11434/api/chat"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": question}]
        }
        async with session.post(url, json=payload) as response:
            if response.status == 404:
                await websocket.send_text("Endpoint not found. Please check the URL and try again.")
                return 
            async for line in response.content:
                #  logging.info(f"Received line: {line}")
                 try: 
                     data = json.loads(line)
                     logging.info(f"Decoded data: {data}")
                     message_content = data['message']['content']
                     await websocket.send_text(message_content)
                
                 except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON: {e}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response_content = await fetch_response("llama3.2:3b", data, websocket)
            if response_content:
                await websocket.send_text(response_content)
                await asyncio.sleep(0.1)
        
    except WebSocketDisconnect:
        print("Client disconnected")
