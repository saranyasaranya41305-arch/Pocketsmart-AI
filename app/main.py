from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
import os

app = FastAPI()

# Find templates - try all possible places
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

possible_paths = [
    ROOT_DIR / "templates",
    BASE_DIR / "templates", 
    Path("templates"),
    Path("app/templates")
]

templates_dir = None
for p in possible_paths:
    if p.exists() and (p / "index.html").exists():
        templates_dir = p
        print(f"FOUND TEMPLATES AT: {p}")
        break

if templates_dir:
    templates = Jinja2Templates(directory=str(templates_dir))
else:
    templates = None
    print("TEMPLATES NOT FOUND! Checked:", possible_paths)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    if templates:
        try:
            return templates.TemplateResponse("index.html", {"request": request})
        except Exception as e:
            print(f"TEMPLATE ERROR: {e}")
            return HTMLResponse(f"<h1>Error: {e}</h1><p>Templates dir: {templates_dir}</p>", status_code=500)
    return {"message": "PocketSmartAI Running", "status": "API is live!", "docs": "/docs", "templates_dir": str(templates_dir), "checked": [str(p) for p in possible_paths]}

@app.get("/api/expenses")
async def get_expenses():
    return []

@app.post("/api/expenses")
async def add_expense(data: dict):
    return data
