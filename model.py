import random

def predict_winner(home_team, away_team, sport):
    # Normalize inputs to keep them consistent
    home = home_team.strip()
    away = away_team.strip()
    
    # THE ARCHITECT'S SECRET SAUCE:
    # We use the team names to create a "seed". 
    # This ensures the prediction stays the same if you ask twice (consistency),
    # but still feels random between different matchups.
    match_seed = hash(home + away + sport)
    random.seed(match_seed)
    
    # 1. Determine Winner (50/50 base logic)
    # We generate a "power level" for each team
    home_power = random.randint(0, 100)
    away_power = random.randint(0, 100)
    
    if home_power > away_power:
        winner = home
        # Calculate confidence based on the gap in power
        confidence = 50 + (home_power - away_power) / 2
    else:
        winner = away
        confidence = 50 + (away_power - home_power) / 2
        
    # Cap confidence so it's never 100% (sports are unpredictable!)
    confidence = min(99, max(51, confidence))

    # 2. Generate Realistic Scores based on the Sport
    if sport == "NBA" or sport == "NCAAB":
        # Basketball: High scores (100+)
        score_winner = random.randint(105, 135)
        score_loser = score_winner - random.randint(1, 15)
        
    elif sport == "NFL":
        # Football: Touchdown/Field goal math
        score_winner = random.choice([21, 24, 27, 30, 31, 34, 38])
        score_loser = score_winner - random.choice([3, 7, 10, 14])
        
    elif sport == "MLB" or sport == "NHL":
        # Baseball/Hockey: Low scores (Runs/Goals)
        score_winner = random.randint(3, 8)
        score_loser = score_winner - random.randint(1, 3)
        
    else:
        # Fallback
        score_winner = 0
        score_loser = 0

    return {
        "matchup": f"{away} @ {home}",
        "sport": sport,
        "predicted_winner": winner,
        "predicted_score": f"{score_winner} - {score_loser}",
        "confidence": f"{int(confidence)}%"
    }