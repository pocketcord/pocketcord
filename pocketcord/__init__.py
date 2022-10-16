from urllib.parse import urlparse

from discord_typings import HeartbeatCommand as Heartbeat, IdentifyData
from disfake import State, User
from quart import Quart, request, websocket

from .core.dispatcher import Dispatcher
from .core.enums import Opcode

dispatcher = Dispatcher()
app = Quart("pocketcord")


@app.get("/gateway")
async def get_gateway():
    parsed_url = urlparse(request.url)
    host = parsed_url.netloc
    return {"url": f"ws://{host}/ws"}


@app.get("/gateway/bot")
async def get_gateway_bot():
    parsed_url = urlparse(request.url)
    host = parsed_url.netloc
    return {
        "url": f"ws://{host}/ws",
        "shards": 1,
        "session_start_limit": {"total": 1000, "remaining": 1000, "reset_after": 0},
    }


async def recv():
    while True:
        data = await websocket.receive_json()
        await dispatcher.dispatch(Opcode(data["op"]), data)


@dispatcher.listen(Opcode.HEARTBEAT)
async def heartbeat(data: Heartbeat) -> None:
    print("heartbeat")
    await websocket.send_json({"op": Opcode.HEARTBEAT_ACK.value})


@dispatcher.listen(Opcode.IDENTIFY)
async def identify(data: IdentifyData) -> None:
    user = User(State(0, 0))
    await websocket.send_json(
        {
            "op": Opcode.DISPATCH.value,
            "t": "READY",
            "s": 0,
            "d": {
                "v": 9,
                "user": user.generate(),
                "guilds": [],
                "session_id": "123",
                "resume_gateway_url": "ws://localhost:5000/ws",
                "application": {
                    "id": "123",
                    "flags": 0,
                },
            },
        }
    )


@app.websocket("/ws")  # type: ignore
async def gateway():
    await websocket.accept()  # type: ignore
    await websocket.send_json(
        {"op": 10, "d": {"heartbeat_interval": 41250, "_trace": ["pocketcord-gateway"]}}
    )
    await recv()
