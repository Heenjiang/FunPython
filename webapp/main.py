from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, status
from typing import Dict
import datetime
import json
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from starlette.websockets import WebSocketState
from pydantic import BaseModel
import logging

# logging configu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chatApp")

SECRET_KEY = "saltedChatAppSecret"
ALGORITHM = "HS256"

app = FastAPI()

class ChatManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.usernames: Dict[str, str] = {}

    async def connect_user(self, websocket: WebSocket, username: str, token: str):
        # Check if the token was used
        if token in self.active_connections:
            logger.warning(f"Token reuse attemption by user '{username}'.")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This token was use.")
        await websocket.accept()
        # Store token and connection detail
        self.active_connections[token] = websocket
        self.usernames[token] = username
        logger.info(f"User '{username}' connected.")
        # Broadcast the new user joining the chat channel
        await self.broadcast_message(f"{username} has joined the chat!", is_notification=True)

    def disconnect_user(self, token: str):
        # the websocket connection already closed, so we need to clean up all resoucers relates to this connection
        if token in self.active_connections:
            websocket = self.active_connections.pop(token)
            username = self.usernames.pop(token, "Unknown user")
            if websocket.client_state != WebSocketState.DISCONNECTED:
                logger.info(f"User '{username}' disconnected.")
                return username
        return None

    async def broadcast_message(self, message: str, sender: WebSocket = None, is_notification: bool = False):
        # Prepare the message to be sent to all users
        message_type = "notification" if is_notification else "message"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_payload = {
            "type": message_type,
            "timestamp": timestamp,
            "content": message
        }
        message_json = json.dumps(message_payload)
        # Send the message to all users except the sender
        for connection in self.active_connections.values():
            if connection != sender:
                await connection.send_text(message_json)
        logger.debug(f"Broadcasted message: {message_payload}")


class TokenRequest(BaseModel):
    username: str

@app.websocket("/ws/{username}")
async def chat_endpoint(websocket: WebSocket, username: str):
    auth_header = websocket.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning("Missing or invalid Authorization header.")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    token = auth_header.split(' ')[1]
    if not token:
        logger.warning("Token not existiing in Authorization header.")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    try:
        # Validate the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("username") != username:
            logger.warning(f"Username and token mismatch: token username '{payload.get('username')}', username in URL '{username}'.")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token!.")
        # Connect the user to the chat
        await chat_manager.connect_user(websocket, username, token)
        while True:
            data = await websocket.receive_text()
            # Broadcast the received message to all other users
            chat_message = f"{username}: {data}"
            await chat_manager.broadcast_message(chat_message, sender=websocket)
    except WebSocketDisconnect:
        # Handle user disconnection
        disconnected_username = chat_manager.disconnect_user(token)
        if disconnected_username:
            logger.info(f"User '{disconnected_username}' disconnected.")
            await chat_manager.broadcast_message(f"{disconnected_username} left the chat.", is_notification=True)
    except ExpiredSignatureError:
        logger.warning(f"Expired token for user '{username}'.")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    except InvalidTokenError:
        logger.warning(f"Invalid token for user '{username}'.")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

@app.post("/token")
async def get_token(request: TokenRequest):
    # Generate a JWT token for the user (username from the POST request)
    payload = {
        "username": request.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    # User bearer token
    bearer_token = f"Bearer {token}"
    logger.info(f"Generating token for user '{request.username}'.")
    return {"token": bearer_token}

# Initialize the chat manager
chat_manager = ChatManager()

# uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem
