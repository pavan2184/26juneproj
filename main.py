from fastapi import FastAPI
from routes import authentication, chat

app = FastAPI()

app.include_router(authentication.router)
app.include_router(chat.router, prefix="/chat")
