from fastapi import FastAPI, HTTPException
import json

from pydanticModel import *
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

@app.post("/clear_chat")
def clear_chat_endpoint(Input: ClearChatInput):
    """
    Endpoint to clear the chat history for a specific conversation.
    
    Parameters:
        conversation_id (str): The ID of the conversation to clear.
    
    Returns:
        dict: Confirmation message indicating the chat has been cleared.
    """
    
    global all_conversations

    conversation_id = Input.conversation_id
    if conversation_id in all_conversations:
        del all_conversations[conversation_id]
        return {"message": "Chat history cleared successfully."}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found.")

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
        response = run_query_and_get_data(current_conversation)
        return {
            "output": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8005)