from channels.consumer import AsyncConsumer
import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class PresentationUpdateConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("moderators",self.channel_name)
        print(f"connected  to {self.channel_name}")

    async def disconnect(self):
        await self.channel_layer.group_discard("moderators", self.channel_name)

    async def moderator_announce(self, event):
        await self.send_json(event)
