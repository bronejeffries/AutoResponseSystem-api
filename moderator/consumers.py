from channels.consumer import AsyncConsumer
import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class PresentationUpdateConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(f"moderator_{self.scope['url_route']['kwargs']['name']}",self.channel_name)
        print(f"connected  to {self.channel_name}\nmoderator_{self.scope['url_route']['kwargs']['name']}")

    async def disconnect(self):
        try:
            await self.channel_layer.group_discard(f"moderator_{self.scope['url_route']['kwargs']['name']}", self.channel_name)
        except Exception:
            prin("Exception occured")

    async def moderator_announce(self, event):
        await self.send_json(event)
