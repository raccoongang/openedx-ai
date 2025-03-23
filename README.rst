OpenEdx AI service
====================================

This repository contains the edX AI Service, which provides web sockets to communicate with AI's.

How to start
------------

1) Clone the repo
2) Install requirements

```
pip install -r requirements.txt
```

3) Run the server with `daphne`

```
daphne -b 127.0.0.1 -p 8002 openedx_ai.asgi:application
```

How to use
----------
Once the server is running, you can connect to the websocket at `ws://127.0.0.1:8002/ws/chatgpt/course-v1:RG+1+1` and send a message.