import requests
import sqlite3
import os

# The high-fidelity feeds
FEEDS = {
    "NCAAB": "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard",
    "NBA": "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
}

def run_sync():
    # LOOK UP ONE LEVEL for the memory bank
    db_path = os.path.join(os.path.dirname(__file__), '..', 'architect_memory.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sport TEXT,
            home_team TEXT,
            away_team TEXT,
            date TEXT,
            status TEXT,
            spread REAL DEFAULT 0.0
        )
    ''')

    for sport, url in FEEDS.items():
        try:
            data = requests.get(url).json()
            for event in data.get('events', []):
                comp = event['competitions'][0]
                home = comp['competitors'][0]['team']['displayName']
                away = comp['competitors'][1]['team']['displayName']
                
                cursor.execute('''
                    INSERT OR REPLACE INTO schedule (sport, home_team, away_team, date, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (sport.upper(), home, away, event['date'], event['status']['type']['description']))
            print(f"// {sport} Sync Complete.")
        except Exception as e:
            print(f"// {sport} Sync Error: {e}")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_sync()