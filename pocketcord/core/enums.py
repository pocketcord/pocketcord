from enum import IntEnum


class Opcode(IntEnum):
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST = 8
    INVALID = 9
    HELLO = 10
    HEARTBEAT_ACK = 11
