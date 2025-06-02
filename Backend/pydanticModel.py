from pydantic import BaseModel

class inputModel(BaseModel):
    """
    Model for input data.
    """
    role: str = "user"
    message: str
    conversation_id: str

class ClearChatInput(BaseModel):
    conversation_id: str