from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine

app = FastAPI()
engine = create_engine("sqlite:///./app.db")

def init_db():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def home():
    return {"message": "PocketSmartAI Running"}