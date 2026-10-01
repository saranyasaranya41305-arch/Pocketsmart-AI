from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

# Find index.html
for p in [ROOT_DIR / "templates" / "index.html", BASE_DIR / "templates" / "index.html", Path("templates/index.html"), Path("app/templates/index.html")]:
    if p.exists():
        INDEX_PATH = p
        break
else:
    INDEX_PATH = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    if INDEX_PATH and INDEX_PATH.exists():
        return HTMLResponse(INDEX_PATH.read_text(encoding="utf-8"))
    return HTMLResponse(f"<h1>Template not found</h1><p>Checked paths, found: {INDEX_PATH}</p>", status_code=500)

@app.get("/api/expenses")
async def get_expenses():
    return []

@app.post("/api/expenses")
async def add_expense(data: dict):
    return data
