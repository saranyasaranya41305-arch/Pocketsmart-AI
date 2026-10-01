from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
from datetime import datetime
from pathlib import Path

app = FastAPI(title="PocketSmartAI")

# DB
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

# FIX: find templates folder correctly
BASE_DIR = Path(__file__).resolve().parent.parent
POSSIBLE_TEMPLATE_DIRS = [BASE_DIR / "templates", Path("templates"), Path("app/templates"), BASE_DIR / "app" / "templates"]

templates = None
for t_dir in POSSIBLE_TEMPLATE_DIRS:
    if t_dir.exists():
        templates = Jinja2Templates(directory=str(t_dir))
        print(f"Templates found at: {t_dir}")
        break

@app.get("/")
def home(request: Request):
    if templates:
        try:
            return templates.TemplateResponse("index.html", {"request": request})
        except Exception as e:
            print(f"Template error: {e}")
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
