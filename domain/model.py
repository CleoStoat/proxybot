from dataclasses import dataclass


@dataclass()
class CopiedMessage:
    origin_chat_id: int
    origin_message_id: int
    copied_message_id: int

@dataclass()
class ProxyChat:
    chat_id: int
    name: str
    listening: bool = True

