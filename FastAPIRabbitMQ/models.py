# models.py
# ──────────────────────────────────────────────────────────────────────
#  Common data model that is used by both the publisher and the consumer.
# ──────────────────────────────────────────────────────────────────────
from pydantic import BaseModel, Field

class Message(BaseModel):
    """The payload that the publisher will send and the consumer will receive."""
    user_id: int = Field(..., example=42)
    action: str = Field(..., example="created")
    data: dict = Field(..., example={"title": "Hello world"})
