import sqlite3
import os
from datetime import datetime, timedelta
from pathlib import Path

def get_db_path():
    """Cross-platform database path resolution"""
    base_dir = Path(__file__).parent.parent
    return base_dir / "architect_memory.db"

def get_forge_db_path():
    """Cross-platform forge database path resolution"""
    base_dir = Path(__file__).parent.parent
    return base_dir / "forge.db"

def init_databases():
    """Initialize both databases with required tables"""
    # architect_memory.db
    conn = sqlite3.connect(str(get_db_path()))
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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS team_stats (
            team_name TEXT PRIMARY KEY,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            points_for REAL DEFAULT 0.0,
            points_against REAL DEFAULT 0.0,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prophecy_logs (
            match_key TEXT PRIMARY KEY,
            winner TEXT,
            confidence TEXT,
            home_rating REAL,
            away_rating REAL,
            prophecy TEXT,
            tier TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citizen_id TEXT,
            entry_time TEXT,
            access_point TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # forge.db
    conn = sqlite3.connect(str(get_forge_db_path()))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citizens (
            citizen_id TEXT PRIMARY KEY,
            access_code TEXT,
            fusion_cores REAL DEFAULT 1000.0,
            accuracy_rating REAL DEFAULT 50.0
        )
    ''')
    
    conn.commit()
    conn.close()

def get_fatigue_penalty(team_name, current_game_date_str):
    """Detect back-to-back games (25 point ELO penalty if tired)"""
    if not current_game_date_str:
        return 0
    
    try:
        conn = sqlite3.connect(str(get_db_path()))
        cursor = conn.cursor()
        
        current_date = datetime.strptime(current_game_date_str[:10], '%Y-%m-%d')
        yesterday = (current_date - timedelta(days=1)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT COUNT(*) FROM schedule
            WHERE (home_team = ? OR away_team = ?)
            AND date LIKE ?
        ''', (team_name, team_name, f"{yesterday}%"))
        
        played_yesterday = cursor.fetchone()[0] > 0
        conn.close()
        
        return 25 if played_yesterday else 0
    except Exception as e:
        print(f"[WARNING] Fatigue penalty calculation failed: {e}")
        return 0
