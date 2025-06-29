import json
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import requests
from jwttoken import JWTBearer, verify_token
from database import chat_collection  

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    question: str
    answer: str

# Endpoint to ask medical questions, store chat with user_id
@router.post("/ask", response_model=ChatResponse)
def ask_medical_question(q: ChatRequest, user_info: str = Depends(verify_token)):
     # Instruction given to Ollama to answer only medical-related qns and instructs what to answer if a non-medical related qn is asked   
    system_prompt = (
        "You are a helpful medical assistant that ONLY answers medical-related questions. "
        "If the question is outside medical context, reply with: "
        "'I'm sorry, I can only answer medical-related questions.'"
    ) 

    # Combine system prompt and user's question in one text
    prompt = system_prompt + "\nUser question: " + q.question

    # prepares the JSON preload with model name that will be used, prompt text and the maximum number of tokens ollama will use to answer the qn
    payload = {
        "model": "medbot:latest",   
        "prompt": prompt,
        "max_tokens": 256
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload) # post request is sent to ollama
        response.raise_for_status() # checks if request is successful
        raw_text = response.text # gets the raw ollama response

        lines = raw_text.strip().split("\n") # splits response answers in new lines

        full_answer = ""
        for line in lines:
            chunk = json.loads(line)
            full_answer += chunk.get("response", "")
            if chunk.get("done", False):
                break

        # Clean \n and \\n into spaces
        full_answer = full_answer.replace("\\n", " ").replace("\n", " ")

        # Store chat history in MongoDB with user email as user_id
        chat_collection.insert_one({
            "user_id": user_info["user_id"],
            "prompt": q.question,
            "response": full_answer,
            "timestamp":  
                __import__('datetime').datetime.now()
        })

        return {"question": q.question, "answer": full_answer} # returns json object with original qn and ollama's answer

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")


# Endpoint to get previous chat history for the user
@router.get("/get_previous_chat/{user_id}")
def get_previous_chat(user_id: str):
    chats = chat_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(20)  # last 20 chats
    
    chat_history = []
    for chat in chats:
        chat_history.append({
            "question": chat.get("prompt"),
            "answer": chat.get("response"),
            "timestamp": chat.get("timestamp")
        })

    return {"user_id": user_id, "chat_history": chat_history}
