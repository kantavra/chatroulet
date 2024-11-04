from fastapi.websockets import WebSocket
import random

class MeetingManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.waiting_users: list[str] = []

    async def add_user(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id] = websocket
        self.waiting_users.append(user_id)

        if len(self.waiting_users) >= 2:
            # Соединяем двух случайных пользователей
            user1 = self.waiting_users.pop(random.randint(0, len(self.waiting_users) - 1))
            user2 = self.waiting_users.pop(random.randint(0, len(self.waiting_users) - 1))
            await self.start_chat(user1, user2)

    async def start_chat(self, user1: str, user2: str):
        # Логика для начала чата между user1 и user2
        message = {"type": "START_CHAT", "user1": user1, "user2": user2}
        await self.active_connections[user1].send_json(message)
        await self.active_connections[user2].send_json(message)

    async def handle_offer(self, user_id: str, offer):
        # Отправляем предложение другому пользователю
        for uid, connection in self.active_connections.items():
            if uid != user_id:
                await connection.send_json({"offer": offer})

    async def handle_answer(self, user_id: str, answer):
        # Отправляем ответ обратно
        for uid, connection in self.active_connections.items():
            if uid != user_id:
                await connection.send_json({"answer": answer})

    async def handle_ice_candidate(self, user_id: str, ice_candidate):
        # Отправляем ICE-кандидат другому пользователю
        for uid, connection in self.active_connections.items():
            if uid != user_id:
                await connection.send_json({"iceCandidate": ice_candidate})

    def remove_user(self, user_id: str, websocket: WebSocket):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            if user_id in self.waiting_users:
                self.waiting_users.remove(user_id)
