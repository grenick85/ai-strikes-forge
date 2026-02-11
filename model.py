import os
import sqlite3
import math
from google import genai
from dotenv import load_dotenv

# Importing from your project structure
try:
    from utils.config import get_fatigue_penalty
except ImportError:
    # Fallback to avoid crashes if the utils folder is moved
    def get_fatigue_penalty(team, date): return 0 

load_dotenv()

class ArchitectModel:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key, http_options={'api_version': 'v1beta'})
        
        # Establishing a dynamic path for your Sports_predictions directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, "architect_memory.db")
        self._init_cache()

    def _init_cache(self):
        conn = sqlite3.connect(self.db_path)
        # Force table structure with match_key 
        conn.execute('''CREATE TABLE IF NOT EXISTS prophecy_logs 
                        (match_key TEXT PRIMARY KEY, winner TEXT, confidence TEXT, 
                         home_rating REAL, away_rating REAL, prophecy TEXT, tier TEXT)''')
        
        # AUTOMATIC REPAIR: Check for the match_key column 
        cursor = conn.execute("PRAGMA table_info(prophecy_logs)")
        columns = [column[1] for column in cursor.fetchall()]
        if "match_key" not in columns:
            print("[ SYSTEM ALERT ]: Table mismatch detected. Rebuilding prophecy_logs...")
            conn.execute("DROP TABLE prophecy_logs")
            conn.execute('''CREATE TABLE prophecy_logs 
                            (match_key TEXT PRIMARY KEY, winner TEXT, confidence TEXT, 
                             home_rating REAL, away_rating REAL, prophecy TEXT, tier TEXT)''')
        
        conn.commit()
        conn.close()

    def get_combat_stats(self, team):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Pulling stats for ELO calculation 
        c.execute("SELECT wins, losses, points_for, points_against FROM team_stats WHERE team_name = ?", (team,))
        stats = c.fetchone() or (10, 10, 110, 110)
        conn.close()
        return stats

    def get_tiered_prediction(self, home, away, tier="Tactical Advantage"):
        match_key = f"{home}_vs_{away}_{tier}"
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 1. CHECK CACHE FOR EXISTING PROPHECY 
        c.execute("SELECT winner, confidence, home_rating, away_rating, prophecy FROM prophecy_logs WHERE match_key=?", (match_key,))
        cached = c.fetchone()
        if cached:
            conn.close()
            return {
                "winner": cached[0], "confidence": cached[1], "home_rating": cached[2],
                "away_rating": cached[3], "prophecy": cached[4], "status": "CACHED", "tier": tier
            }

        # 2. PERFORM ELO MATH 
        h_stats = self.get_combat_stats(home)
        a_stats = self.get_combat_stats(away)
        
        r_home = 1500 + ((h_stats[0] - h_stats[1]) * 10)
        r_away = 1500 + ((a_stats[0] - a_stats[1]) * 10)

        # Apply fatigue penalty for today's date 
        r_home -= get_fatigue_penalty(home, "2026-02-09")
        r_away -= get_fatigue_penalty(away, "2026-02-09")

        prob = 1.0 / (1.0 + math.pow(10, (r_away - r_home) / 400.0))
        winner = home if prob > 0.5 else away
        confidence = f"{round(prob * 100 if prob > 0.5 else (1 - prob) * 100, 2)}%"

        # 3. GENERATE AI PROPHECY 
        try:
            prompt = f"LEVEL: {tier}. MATCHUP: {home} vs {away}. WINNER: {winner} ({confidence}). GIVE A CRYPTIC PROPHECY."
            ai_resp = self.client.models.generate_content(model="models/gemini-2.0-flash", contents=prompt)
            prophecy = ai_resp.text
            
            c.execute("INSERT OR REPLACE INTO prophecy_logs VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (match_key, winner, confidence, r_home, r_away, prophecy, tier))
            conn.commit()
            status = "SUCCESS"
        except Exception as e:
            print(f"AI CONNECTION FAILED: {e}")
            prophecy = "BRAIN OVERHEATED. COOLDOWN ACTIVE."
            status = "COOLDOWN"

        conn.close()
        return {"winner": winner, "confidence": confidence, "prophecy": prophecy, "status": status, "tier": tier}