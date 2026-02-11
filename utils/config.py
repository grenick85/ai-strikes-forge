import sqlite3
import os
from datetime import datetime, timedelta

def get_fatigue_penalty(team_name, current_game_date_str):
    """
    Scans architect_memory.db to detect physical decay (Back-to-Back games).
    """
    if not current_game_date_str:
        return 0
        
    try:
        # Absolute path to ensure it finds the memory bank
        db_path = r"C:\Users\nicky\sports_predictions\architect_memory.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Converts ISO date '2026-02-08T00:00Z' to a math-ready format
        current_date = datetime.strptime(current_game_date_str[:10], '%Y-%m-%d')
        yesterday = (current_date - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Query the schedule table for any game involving this team yesterday
        cursor.execute('''
            SELECT COUNT(*) FROM schedule 
            WHERE (home_team = ? OR away_team = ?) 
            AND date LIKE ?
        ''', (team_name, team_name, f"{yesterday}%"))
        
        played_yesterday = cursor.fetchone()[0] > 0
        conn.close()
        
        # Returns a 25-point Elo penalty if they are tired
        return 25 if played_yesterday else 0
    except Exception as e:
        return 0