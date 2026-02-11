import os
import sqlite3
import uvicorn
import datetime
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model import ArchitectModel

app = FastAPI(title="AI STRIKES - THE FORGE")
model = ArchitectModel()

# --- Directory Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
FORGE_DB = os.path.join(BASE_DIR, "forge.db")
MEMORY_DB = os.path.join(BASE_DIR, "architect_memory.db")

# Ensure static files (CSS/JS) and templates are served from the /static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=STATIC_DIR)

# --- 1. The Entrance (Login) ---
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# --- 2. The Sentry (Authentication) ---
@app.post("/authenticate")
async def auth(citizen_id: str = Form(...), access_code: str = Form(...)):
    conn = sqlite3.connect(FORGE_DB)
    user = conn.execute("SELECT citizen_id FROM citizens WHERE citizen_id=? AND access_code=?", 
                        (citizen_id, access_code)).fetchone()
    conn.close()
    
    if user: 
        return RedirectResponse(url=f"/hub/{citizen_id}", status_code=303)
    raise HTTPException(status_code=401, detail="Unauthorized Access to the Vault")

# --- 3. The Hub & Scribe (Memory Logging) ---
@app.get("/hub/{email_or_id:path}", response_class=HTMLResponse)
async def vault_hub(request: Request, email_or_id: str):
    target_id = "Nicky" if "@" in email_or_id else email_or_id
    
    try:
        mem_conn = sqlite3.connect(MEMORY_DB)
        mem_conn.execute("""
            CREATE TABLE IF NOT EXISTS access_logs 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, citizen_id TEXT, entry_time TEXT, access_point TEXT)
        """)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mem_conn.execute(
            "INSERT INTO access_logs (citizen_id, entry_time, access_point) VALUES (?, ?, ?)",
            (target_id, timestamp, "Cloudflare Tunnel" if "@" in email_or_id else "Local Forge")
        )
        mem_conn.commit()
        mem_conn.close()
    except Exception as e:
        print(f"Scribe Warning: {e}")

    conn = sqlite3.connect(FORGE_DB)
    citizen_data = conn.execute("SELECT citizen_id, fusion_cores FROM citizens WHERE citizen_id=?", 
                                (target_id,)).fetchone()
    conn.close()
    
    if not citizen_data:
        return RedirectResponse(url="/")
        
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "citizen_id": citizen_data[0],
        "fusion_cores": citizen_data[1]
    })

# --- 4. The Operating Theater (Strikes) ---
@app.post("/strike")
async def strike(home: str = Form(...), away: str = Form(...), citizen_id: str = Form(...), tier: str = Form(...)):
    intel = model.get_tiered_prediction(home, away, tier=tier)
    
    if intel["status"] == "SUCCESS":
        costs = {"Tactical Advantage": 0.5, "Eyes in the Sky": 1.0, "Cyber-nuked": 2.0}
        cost = costs.get(tier, 0.5)
        
        conn = sqlite3.connect(FORGE_DB)
        conn.execute("UPDATE citizens SET fusion_cores = fusion_cores - ? WHERE citizen_id=?", 
                     (cost, citizen_id))
        conn.commit()
        conn.close()
        
    return {"status": intel["status"], "intel": intel}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)