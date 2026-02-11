import os
import sqlite3
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
API_KEY = os.getenv("APISPORTS_KEY")
DB_PATH = r"C:\Users\nicky\sports_predictions\architect_memory.db"

# API-Sports Tactical Endpoints
ENDPOINTS = {
    "NBA": "https://v2.nba.api-sports.io/games",
    "SOCCER": "https://v3.football.api-sports.io/fixtures"
}

def init_memory():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS schedule 
                 (game_id INTEGER PRIMARY KEY, home_team TEXT, away_team TEXT, 
                  date TEXT, status TEXT, sport TEXT, spread REAL DEFAULT 0.0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS team_stats 
                 (team_name TEXT PRIMARY KEY, wins INTEGER, losses INTEGER, 
                  points_for REAL, points_against REAL)''')
    conn.commit()
    conn.close()

def scan_network(sport):
    print(f"[ INITIALIZING {sport} SCAN... ]")
    headers = {'x-apisports-key': API_KEY}
    
    # recalibrating parameters for Free Plan and Data Structures
    if sport == "NBA":
        # Scanning for a known date to ensure data presence
        params = {"date": "2024-02-08"} 
    else: 
        # SOCCER: Adjusting to 2024 season to bypass Free Plan restriction
        params = {"league": "39", "season": "2024", "next": "10"}

    try:
        response = requests.get(ENDPOINTS[sport], headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('errors'):
                print(f"[ VAULT ERROR: {data['errors']} ]")
                return

            results = data.get('response', [])
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            for item in results:
                if sport == "NBA":
                    # NBA uses 'visitors' instead of 'away'
                    gid = item['id']
                    home = item['teams']['home']['name']
                    away = item['teams']['visitors']['name'] 
                    status = item['status']['long']
                    date = item['date']['start']
                else: # Soccer
                    gid = item['fixture']['id']
                    home = item['teams']['home']['name']
                    away = item['teams']['away']['name']
                    status = item['fixture']['status']['long']
                    date = item['fixture']['date']

                c.execute("""INSERT OR REPLACE INTO schedule 
                             (game_id, home_team, away_team, date, status, sport) 
                             VALUES (?, ?, ?, ?, ?, ?)""",
                          (gid, home, away, date, status, sport))
            
            conn.commit()
            conn.close()
            print(f"[ SUCCESS: {len(results)} {sport} TARGETS ACQUIRED ]")
        else:
            print(f"[ ACCESS DENIED: {response.status_code} ]")
    except Exception as e:
        print(f"[ CRITICAL SENSOR FAILURE: {e} ]")

if __name__ == "__main__":
    init_memory()
    scan_network("NBA")
    scan_network("SOCCER")