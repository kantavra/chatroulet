from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from signaling.manager import MeetingManager
import json
import random

websocket_router = APIRouter()
meeting_manager = MeetingManager()

@websocket_router.websocket("/ws")
async def connect_websocket(websocket: WebSocket):
    await websocket.accept()
    user_id = str(random.randint(1, 10000))  # Генерация уникального ID для пользователя
    await meeting_manager.add_user(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()  # Получаем текстовые данные
            message = json.loads(data)  # Декодируем JSON

            # Обрабатываем разные типы сообщений
            if "offer" in message:
                await meeting_manager.handle_offer(user_id, message["offer"])
            elif "answer" in message:
                await meeting_manager.handle_answer(user_id, message["answer"])
            elif "iceCandidate" in message:
                await meeting_manager.handle_ice_candidate(user_id, message["iceCandidate"])

    except WebSocketDisconnect:
        meeting_manager.remove_user(user_id, websocket)
