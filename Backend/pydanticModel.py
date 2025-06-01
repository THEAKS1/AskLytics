from pydantic import BaseModel

class inputModel(BaseModel):
    """
    Model for input data.
    """
    role: str = "user"
    message: str
    conversation_id: str

class outputModel(BaseModel):
    """
    Model for output data.
    """
    message: str
    role: str = "assistant"
    status: str = "success"