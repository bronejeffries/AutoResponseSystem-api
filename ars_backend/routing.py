from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django.conf.urls import url
from moderator.consumers import PresentationUpdateConsumer


application = ProtocolTypeRouter({
    "websocket": URLRouter([
        url(r'^moderator/session/category/presentations/(?P<name>[a-zA-Z0-9_.]+)/$',PresentationUpdateConsumer)
    ])
})
