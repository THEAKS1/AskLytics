from fastapi import FastAPI, HTTPException
import json

from pydanticModel import inputModel, outputModel
from helper import get_or_create_conversation
from chat import *

app = FastAPI()

all_conversations = {}

@app.get("/health-check")
def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "ok", "message": "Service is running."}

@app.post("/chat")
def chat_endpoint(input_data: inputModel):
    """
    Endpoint to handle chat requests.
    """

    global all_conversations

    conversation_id = input_data.conversation_id
    current_conversation = get_or_create_conversation(conversation_id, all_conversations)

    # Append the new message to the conversation history
    current_conversation.messages.append({
        "role": input_data.role,
        "content": input_data.message
    })
    print(f"Current conversation messages: {current_conversation.messages[-1]}")
    # Call the chat function with the current conversation
    try:
        response = driver_function(current_conversation)
        return {
            "output": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8005)