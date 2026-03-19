from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
client=Groq(api_key=api_key)

class chat_struc(BaseModel):
    session_id:str
    message:str

sessions={}

app=FastAPI()

@app.get("/")
def root():
    return{'Message':"api is running"}

@app.post("/chats")
def create_chat(chat:chat_struc):
    global sessions   
    session_id=chat.session_id
    if session_id not in sessions:
        sessions[session_id] = []
    message=chat.message
    sessions[session_id].append({"role":"user","content":message})
    chat_completion=client.chat.completions.create(
        messages=sessions[session_id],
        model="llama-3.3-70b-versatile",
    )
    response=chat_completion.choices[0].message.content
    sessions[session_id].append({"role":"assistant","content":response})
    return response
        
@app.delete("/chats/{session_id}")
def delete_chat(session_id:str):
    global sessions
    if session_id not in sessions:
        raise HTTPException(status_code=404,detail="chat not found")
    deleted_chat=sessions.pop(session_id)
    return {"Message":"Chat deleted","session id":session_id}
