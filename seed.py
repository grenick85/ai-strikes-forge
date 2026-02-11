import sqlite3
def seed_architect():
    conn = sqlite3.connect('forge.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO citizens (citizen_id, access_code, fusion_cores, accuracy_rating) VALUES (?, ?, ?, ?)", 
                  ('nicky@ai-strikes.com', 'Vault716', 1000000.0, 99.9))
        conn.commit()
        print("CITIZEN AUTHENTICATED: The Architect is recognized.")
    except:
        print("ERROR: Citizen already exists.")
    conn.close()
if __name__ == "__main__":
    seed_architect()