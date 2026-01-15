# THE ARCHITECT'S BRAIN (Database + Logic)

# 1. The Data (NFL, NBA, NCAA)
team_stats = {
    # --- NFL ---
    "chiefs": 0.95, "kansas city chiefs": 0.95,
    "49ers": 0.94, "san francisco 49ers": 0.94,
    "ravens": 0.93, "baltimore ravens": 0.93,
    "lions": 0.91, "detroit lions": 0.91,
    "bills": 0.90, "buffalo bills": 0.90,
    "cowboys": 0.88, "dallas cowboys": 0.88,
    "eagles": 0.87, "philadelphia eagles": 0.87,
    "dolphins": 0.85, "miami dolphins": 0.85,
    "browns": 0.82, "cleveland browns": 0.82,
    "packers": 0.80, "green bay packers": 0.80,
    "rams": 0.79, "los angeles rams": 0.79,
    "jaguars": 0.78, "jacksonville jaguars": 0.78,
    "steelers": 0.77, "pittsburgh steelers": 0.77,
    "bengals": 0.76, "cincinnati bengals": 0.76,
    "buccaneers": 0.75, "tampa bay buccaneers": 0.75,
    "seahawks": 0.74, "seattle seahawks": 0.74,
    "colts": 0.72, "indianapolis colts": 0.72,
    "vikings": 0.71, "minnesota vikings": 0.71,
    "bears": 0.65, "chicago bears": 0.65,
    "falcons": 0.64, "atlanta falcons": 0.64,
    "saints": 0.63, "new orleans saints": 0.63,
    "broncos": 0.62, "denver broncos": 0.62,
    "raiders": 0.61, "las vegas raiders": 0.61,
    "jets": 0.60, "new york jets": 0.60,
    "giants": 0.58, "new york giants": 0.58,
    "titans": 0.57, "tennessee titans": 0.57,
    "cardinals": 0.56, "arizona cardinals": 0.56,
    "patriots": 0.55, "new england patriots": 0.55,
    "commanders": 0.54, "washington commanders": 0.54,
    "panthers": 0.50, "carolina panthers": 0.50,

    # --- NBA ---
    "celtics": 0.94, "boston celtics": 0.94,
    "nuggets": 0.93, "denver nuggets": 0.93,
    "bucks": 0.91, "milwaukee bucks": 0.91,
    "timberwolves": 0.90, "minnesota timberwolves": 0.90,
    "lakers": 0.84, "los angeles lakers": 0.84,
    "warriors": 0.83, "golden state warriors": 0.83,
    "bulls": 0.70, "chicago bulls": 0.70,

    # --- NCAA ---
    "michigan": 0.89, "michigan wolverines": 0.89,
    "washington": 0.88, "washington huskies": 0.88,
    "texas": 0.87, "texas longhorns": 0.87,
    "alabama": 0.86, "alabama crimson tide": 0.86,
    "georgia": 0.85, "georgia bulldogs": 0.85,
    "ohio state": 0.80, "ohio state buckeyes": 0.80
}

# 2. The Logic Function
def predict_matchup(home_team, away_team):
    home = home_team.lower().strip()
    away = away_team.lower().strip()

    # Check if teams exist
    if home not in team_stats or away not in team_stats:
        return {"error": "Team not found in database. Check spelling!"}

    # Get stats
    home_strength = team_stats[home]
    away_strength = team_stats[away]

    # Calculate (Home field advantage = +0.1)
    home_total = home_strength + 0.1
    
    if home_total > away_strength:
        winner = home_team
        margin = home_total - away_strength
    else:
        winner = away_team
        margin = away_strength - home_total
    
    # Return a Dictionary (JSON)
    return {
        "matchup": f"{home_team} vs {away_team}",
        "predicted_winner": winner,
        "confidence_level": f"{round(margin * 100, 1)}%",
        "data_source": "The Architect v2.0"
    }