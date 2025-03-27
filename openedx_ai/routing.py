from django.urls import re_path

from .consumers import ChatGPTConsumer

websocket_urlpatterns = [
    re_path(r"ws/chatgpt/(?P<course_id>[^/]+)/$", ChatGPTConsumer.as_asgi()),
]
