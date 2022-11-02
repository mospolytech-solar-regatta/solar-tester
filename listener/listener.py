from redis.asyncio import Redis
from fastapi import WebSocket


class Listener:
    def __init__(self):
        self.redis = Redis()
        self.pubsub = self.redis.pubsub()

    async def listen(self, topic: str, websocket: WebSocket):
        await self.pubsub.subscribe(topic)
        while True:
            msg = await self.pubsub.get_message(ignore_subscribe_messages=True)
            if msg is not None:
                await websocket.send_text(msg['data'])

    async def stop(self):
        await self.redis.close()
