from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.utils import process_user_request
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

class UserRequest(BaseModel):
    user_question: str

@app.post("/chat")
async def chat_api(user_request: UserRequest):
    user_question = user_request.user_question
    try:
        result = process_user_request(user_question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)