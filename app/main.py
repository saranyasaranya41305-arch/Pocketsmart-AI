from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
from datetime import datetime

app = FastAPI(title="PocketSmartAI")

# DB Setup
engine = create_engine("sqlite:///./app.db")

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    amount: float
    category: str = "general"
    created_at: datetime = Field(default_factory=datetime.utcnow)

def init_db():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    init_db()

# Mount static if exists
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")
    HAS_TEMPLATES = True
except:
    HAS_TEMPLATES = False
    templates = None

@app.get("/")
def home(request: Request):
    if HAS_TEMPLATES:
        try:
            return templates.TemplateResponse("index.html", {"request": request})
        except:
            pass
    return {"message": "PocketSmartAI Running", "status": "API is live!", "docs": "/docs"}

@app.get("/api/expenses")
def get_expenses():
    with Session(engine) as session:
        expenses = session.exec(select(Expense)).all()
        return expenses

@app.post("/api/expenses")
def add_expense(expense: Expense):
    with Session(engine) as session:
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "PocketSmartAI"}
