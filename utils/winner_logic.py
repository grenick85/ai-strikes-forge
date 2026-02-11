def predict_winner(home_team, away_team):
    # Get current ratings from the Vault (default to 1500)
    r_home = _ratings.get(home_team, BASE_RATING)
    r_away = _ratings.get(away_team, BASE_RATING)

    # --- THE ARCHITECT'S EDGE: HOME COURT ADVANTAGE ---
    # In NCAAB, playing at home is worth roughly 3.5 to 4 points, 
    # which translates to ~100 Elo points.
    effective_home_rating = r_home + 100

    # Calculate Probability using the Logistic Curve
    # Formula: 1 / (1 + 10^((away - home) / 400))
    exponent = (r_away - effective_home_rating) / 400.0
    win_prob = 1.0 / (1.0 + (10.0 ** exponent))

    # Determine the "Prophecy"
    predicted_winner = home_team if win_prob > 0.5 else away_team
    confidence = win_prob if win_prob > 0.5 else (1.0 - win_prob)

    return {
        "winner": predicted_winner,
        "probability": round(confidence * 100, 2),
        "home_elo": r_home,
        "away_elo": r_away
    }
