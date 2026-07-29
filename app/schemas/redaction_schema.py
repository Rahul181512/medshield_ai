from pydantic import BaseModel


class RedactionRequest(BaseModel):
    text: str


class Entity(BaseModel):
    type: str
    value: str


class RedactionResponse(BaseModel):
    original_text: str
    redacted_text: str
    entities: list[Entity]