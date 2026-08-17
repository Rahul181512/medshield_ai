from pydantic import BaseModel


class Entity(BaseModel):
    type: str
    value: str


class RedactionRequest(BaseModel):
    text: str


class RedactionResponse(BaseModel):
    session_id: str
    original_text: str
    redacted_text: str
    entities: list[Entity]


class RestoreRequest(BaseModel):
    session_id: str
    text: str