import dataclasses

@dataclasses.dataclass
class Message:
    sender_name: str
    content: str