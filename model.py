import json
from datetime import datetime

class ArchitectModel:
    def __init__(self):
        self.madden_ratings = self._load_madden_ratings()

    def _load_madden_ratings(self):
        try:
            with open("madden_ratings.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("[WARNING] madden_ratings.json not found.")
            return {}

    def get_season_stats(self, team_name, start_date):
        """
        The Stats Engine: Pulls the team's averages since the given start_date.
        Focuses heavily on passing, rushing, and turnover differentials.
        """
        print(f"[DATA] Pulling stats for {team_name} from {start_date} onward...")
        
        # In production, this queries your database using the start_date.
        # These represent average yards per game and turnovers.
        mock_db = {
            "Chiefs": {
                "offense": {"pass_yds": 280, "rush_yds": 110, "turnovers": 1.1, "pf": 28.3},
                "defense": {"pass_yds_allowed": 210, "rush_yds_allowed": 105, "turnovers_forced": 1.5, "pa": 21.5},
                "rank": 89,
                "off_pass_stat": 216.6,
                "off_rush_stat": 159.6,
                "def_pass_stat": 156.9,
                "def_rush_stat": 136.2,
            },
            "Ravens": {
                "offense": {"pass_yds": 220, "rush_yds": 160, "turnovers": 0.9, "pf": 17.6},
                "defense": {"pass_yds_allowed": 190, "rush_yds_allowed": 95, "turnovers_forced": 1.8, "pa": 29.6},
                "rank": 83,
                "off_pass_stat": 140.3,
                "off_rush_stat": 123.3,
                "def_pass_stat": 216.1,
                "def_rush_stat": 139.5,
            },
            "Buffalo Bills": {
                "offense": {"pass_yds": 280, "rush_yds": 110, "turnovers": 1.1, "pf": 28.3},
                "defense": {"pass_yds_allowed": 210, "rush_yds_allowed": 105, "turnovers_forced": 1.5, "pa": 21.5},
                "rank": 89,
                "off_pass_stat": 216.6,
                "off_rush_stat": 159.6,
                "def_pass_stat": 156.9,
                "def_rush_stat": 136.2,
            },
            "New York Jets": {
                "offense": {"pass_yds": 220, "rush_yds": 160, "turnovers": 0.9, "pf": 17.6},
                "defense": {"pass_yds_allowed": 190, "rush_yds_allowed": 95, "turnovers_forced": 1.8, "pa": 29.6},
                "rank": 83,
                "off_pass_stat": 140.3,
                "off_rush_stat": 123.3,
                "def_pass_stat": 216.1,
                "def_rush_stat": 139.5,
            }
        }
        return mock_db.get(team_name, {
            "offense": {"pass_yds": 200, "rush_yds": 100, "turnovers": 1.5, "pf": 20.0},
            "defense": {"pass_yds_allowed": 200, "rush_yds_allowed": 100, "turnovers_forced": 1.0, "pa": 21.0},
            "rank": 16,
            "off_pass_stat": 180.0,
            "off_rush_stat": 115.0,
            "def_pass_stat": 190.0,
            "def_rush_stat": 120.0,
        })

    def calculate_matchup_advantage(self, offense_stats, defense_stats):
        """
        The Heartbeat of the Mission. 
        Pits Team A's Offense directly against Team B's Defense.
        """
        # Calculate how the offense's average fares against the defense's allowance
        # A positive number means the offense has the advantage.
        pass_diff = offense_stats["pass_yds"] - defense_stats["pass_yds_allowed"]
        rush_diff = offense_stats["rush_yds"] - defense_stats["rush_yds_allowed"]
        
        # Turnovers are massive swing multipliers. 
        # (Offensive turnovers - Defensive takeaways) * heavy weight
        turnover_battle = (defense_stats["turnovers_forced"] - offense_stats["turnovers"]) * 25 
        
        # Total matchup power score
        matchup_score = pass_diff + rush_diff - turnover_battle
        
        return matchup_score

    def calculate_score_prediction(self, team_stats, opponent_stats, is_home=True):
        """
        Apply the prediction formula to calculate numerical score.
        
        Formula Components (from your spreadsheet):
        - Offensive Pass Yards
        - Offensive Rush Yards
        - Points For (PF)
        - Points Against (PA)
        - Defensive Pass Yards Allowed
        - Defensive Rush Yards Allowed
        - Rank vs Rank differential
        - Pass differential
        - Rush differential
        - Sum of team differential
        - Special math for game outcome
        - Injury adjustment
        """
        
        # Extract stats
        off_pass = team_stats.get("off_pass_stat", 200.0)
        off_rush = team_stats.get("off_rush_stat", 110.0)
        pf = team_stats["offense"].get("pf", 20.0)
        pa = team_stats["defense"].get("pa", 21.0)
        def_pass = team_stats.get("def_pass_stat", 200.0)
        def_rush = team_stats.get("def_rush_stat", 115.0)
        rank = team_stats.get("rank", 16)
        opp_rank = opponent_stats.get("rank", 16)
        
        # Calculate differentials
        pass_diff = off_pass - def_pass
        rush_diff = off_rush - def_rush
        rank_diff = rank - opp_rank  # Home field / strength indicator
        
        # Sum of team differential
        sum_of_differential = pass_diff + rush_diff + rank_diff
        
        # Base score calculation
        base_score = pf + (pass_diff * 0.02) + (rush_diff * 0.03)
        
        # Special math for game outcome (applied multiplier based on matchup)
        matchup_multiplier = 1.0 + (sum_of_differential * 0.001)
        
        # Injury adjustment (default to 0 for now, can be enhanced)
        injury_adjustment = 0
        
        # Final score calculation
        final_score = (base_score * matchup_multiplier) + injury_adjustment
        
        # Ensure realistic NFL score range (0-65)
        final_score = max(0, min(65, final_score))
        
        return round(final_score, 1)

    def get_gamified_prediction(self, team_a, team_b, season_start_date, manual_injuries=None):
        """
        Runs the full dual-sided matchup math and applies Madden penalties if provided.
        """
        if manual_injuries is None:
            manual_injuries = {team_a: [], team_b: []}

        print(f"\n--- INITIATING FORGE MATCHUP: {team_a} vs {team_b} ---")
        print(f"Season Start Marker: {season_start_date}\n")

        # 1. Pull core stats
        stats_a = self.get_season_stats(team_a, season_start_date)
        stats_b = self.get_season_stats(team_b, season_start_date)

        # 2. Clash 1: Team A Offense vs Team B Defense
        a_off_vs_b_def = self.calculate_matchup_advantage(stats_a["offense"], stats_b["defense"])
        
        # 3. Clash 2: Team B Offense vs Team A Defense
        b_off_vs_a_def = self.calculate_matchup_advantage(stats_b["offense"], stats_a["defense"])

        print(f"[CLASH 1] {team_a} Offense vs {team_b} Defense Advantage: {a_off_vs_b_def:.1f} pts")
        print(f"[CLASH 2] {team_b} Offense vs {team_a} Defense Advantage: {b_off_vs_a_def:.1f} pts")

        # 4. Determine Base Differential
        base_differential = a_off_vs_b_def - b_off_vs_a_def

        # 5. Apply Madden Injury Penalties (Manual input for now)
        penalty_a = self._calculate_injury_penalty(team_a, manual_injuries[team_a])
        penalty_b = self._calculate_injury_penalty(team_b, manual_injuries[team_b])

        final_score = base_differential - penalty_a + penalty_b

        # 6. Output the Verdict
        print(f"\n[ADJUSTMENTS] {team_a} Penalty: -{penalty_a} | {team_b} Penalty: -{penalty_b}")
        
        if final_score > 0:
            return f">> PREDICTION: {team_a} holds the numerical advantage (+{final_score:.1f})."
        elif final_score < 0:
            return f">> PREDICTION: {team_b} holds the numerical advantage (+{abs(final_score):.1f})."
        else:
            return ">> PREDICTION: DEAD HEAT. Perfect Matchup."

    def get_tiered_prediction(self, home, away, tier="Tactical Advantage", manual_injuries=None):
        """
        Get a prediction with tiered intelligence levels and NUMERICAL SCORE PREDICTIONS.
        Tier 1 (Tactical Advantage): Basic analysis
        Tier 2 (Eyes in the Sky): Detailed analysis with scores
        Tier 3 (Cyber-nuked): Deep analysis with scores and injury impacts
        """
        if manual_injuries is None:
            manual_injuries = {home: [], away: []}

        print(f"\n--- INITIATING {tier.upper()} PREDICTION ---")
        print(f"Matchup: {home} vs {away}\n")

        # Pull core stats
        home_stats = self.get_season_stats(home, "2026-01-01")
        away_stats = self.get_season_stats(away, "2026-01-01")

        # Calculate score predictions
        home_score = self.calculate_score_prediction(home_stats, away_stats, is_home=True)
        away_score = self.calculate_score_prediction(away_stats, home_stats, is_home=False)

        # Calculate basic matchup
        home_off_vs_away_def = self.calculate_matchup_advantage(home_stats["offense"], away_stats["defense"])
        away_off_vs_home_def = self.calculate_matchup_advantage(away_stats["offense"], home_stats["defense"])

        base_differential = home_off_vs_away_def - away_off_vs_home_def

        # Tier-specific analysis
        if tier == "Tactical Advantage":
            # Basic prediction
            confidence = 65
            prediction = self._generate_prediction(base_differential, home, away)
        
        elif tier == "Eyes in the Sky":
            # Include injury analysis and refine scores
            penalty_home = self._calculate_injury_penalty(home, manual_injuries[home])
            penalty_away = self._calculate_injury_penalty(away, manual_injuries[away])
            adjusted_diff = base_differential - penalty_home + penalty_away
            
            # Adjust scores based on injuries
            home_score = max(0, home_score - penalty_home)
            away_score = max(0, away_score - penalty_away)
            
            prediction = self._generate_prediction(adjusted_diff, home, away)
            confidence = 78
        
        elif tier == "Cyber-nuked":
            # Full analysis with all factors
            penalty_home = self._calculate_injury_penalty(home, manual_injuries[home])
            penalty_away = self._calculate_injury_penalty(away, manual_injuries[away])
            adjusted_diff = base_differential - penalty_home + penalty_away
            
            # Add turnover weighting
            turnover_impact = abs(home_stats["offense"]["turnovers"] - away_stats["offense"]["turnovers"]) * 15
            final_diff = adjusted_diff + turnover_impact
            
            # Adjust scores with all factors
            home_score = max(0, home_score - penalty_home + (turnover_impact * 0.5))
            away_score = max(0, away_score - penalty_away - (turnover_impact * 0.5))
            
            prediction = self._generate_prediction(final_diff, home, away)
            confidence = 89
        
        else:
            confidence = 50
            prediction = self._generate_prediction(base_differential, home, away)

        # Ensure scores are realistic
        home_score = round(max(0, min(65, home_score)), 1)
        away_score = round(max(0, min(65, away_score)), 1)

        return {
            "status": "SUCCESS",
            "intel": prediction,
            "home_team": home,
            "away_team": away,
            "home_score": home_score,
            "away_score": away_score,
            "tier": tier,
            "confidence": f"{confidence}%",
            "matchup_score": f"{base_differential:.2f}",
            "prediction_summary": f"{home} {home_score} - {away_score} {away}"
        }

    def _generate_prediction(self, differential, home, away):
        """Generate a prediction message based on the differential."""
        if differential > 10:
            return f"🎯 {home} has a DOMINANT advantage. Prediction: {home} WINS by 2+ scores."
        elif differential > 0:
            return f"✓ {home} shows statistical superiority. Prediction: {home} WINS."
        elif differential < -10:
            return f"🎯 {away} has a DOMINANT advantage. Prediction: {away} WINS by 2+ scores."
        elif differential < 0:
            return f"✓ {away} shows statistical superiority. Prediction: {away} WINS."
        else:
            return f"⚖️ Perfect statistical matchup. Prediction: TOSS UP / DEAD HEAT."

    def _calculate_injury_penalty(self, team_name, injured_players):
        """Checks the Madden JSON to subtract points for missing Top 5 stars."""
        team_data = self.madden_ratings.get(team_name, {})
        team_average = team_data.get("team_average", 80)
        stars = team_data.get("stars", {})
        
        penalty = 0
        for player in injured_players:
            if player in stars:
                drop = stars[player] - team_average
                penalty += drop
                print(f"[{team_name} ALERT] {player} OUT. Applying -{drop} point penalty.")
        return penalty

# --- Local Execution Test ---
if __name__ == "__main__":
    forge = ArchitectModel()
    
    # Test the tiered prediction
    result = forge.get_tiered_prediction("Chiefs", "Ravens", tier="Eyes in the Sky")
    print(f"\nPrediction Result: {result}")
