import sqlite3
import os

def init_forge_db():
    """Initialize the forge.db with the citizens table if it doesn't exist."""
    DB_PATH = os.path.join(os.path.dirname(__file__), "forge.db")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create citizens table
    c.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            citizen_id TEXT UNIQUE, 
            access_code TEXT, 
            fusion_cores REAL DEFAULT 10.0, 
            accuracy_rating REAL DEFAULT 87.4
        )
    """)
    
    conn.commit()
    conn.close()
    print("[FORGE INITIALIZED] Database schema created.")

def seed_architect():
    """Add the Architect user (developer/admin)."""
    DB_PATH = os.path.join(os.path.dirname(__file__), "forge.db")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute("""
            INSERT INTO citizens (citizen_id, access_code, fusion_cores, accuracy_rating) 
            VALUES (?, ?, ?, ?)
        """, ('Nicky', 'Vault716', 1000.0, 99.9))
        conn.commit()
        print("✓ CITIZEN AUTHENTICATED: The Architect (Nicky) is recognized.")
    except sqlite3.IntegrityError:
        print("⚠ ALERT: The Architect already exists in the vault.")
    finally:
        conn.close()

def seed_test_users():
    """Add test users for development."""
    DB_PATH = os.path.join(os.path.dirname(__file__), "forge.db")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    test_users = [
        ('TestUser1', 'password123', 500.0, 75.0),
        ('TestUser2', 'password456', 750.0, 82.3),
    ]
    
    for citizen_id, access_code, cores, rating in test_users:
        try:
            c.execute("""
                INSERT INTO citizens (citizen_id, access_code, fusion_cores, accuracy_rating) 
                VALUES (?, ?, ?, ?)
            """, (citizen_id, access_code, cores, rating))
        except sqlite3.IntegrityError:
            print(f"⚠ {citizen_id} already exists.")
    
    conn.commit()
    conn.close()
    print("✓ TEST USERS seeded.")

if __name__ == "__main__":
    init_forge_db()
    seed_architect()
    seed_test_users()
    print("\n[SUCCESS] The Forge is ready for deployment.")