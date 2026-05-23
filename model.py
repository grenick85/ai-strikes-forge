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
                "offense": {"pass_yds": 280, "rush_yds": 110, "turnovers": 1.1},
                "defense": {"pass_yds_allowed": 210, "rush_yds_allowed": 105, "turnovers_forced": 1.5}
            },
            "Ravens": {
                "offense": {"pass_yds": 220, "rush_yds": 160, "turnovers": 0.9},
                "defense": {"pass_yds_allowed": 190, "rush_yds_allowed": 95, "turnovers_forced": 1.8}
            }
        }
        return mock_db.get(team_name, {
            "offense": {"pass_yds": 200, "rush_yds": 100, "turnovers": 1.5},
            "defense": {"pass_yds_allowed": 200, "rush_yds_allowed": 100, "turnovers_forced": 1.0}
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
    
    # We set the start date, the teams, and any known injuries manually to test the math
    start_date = "2026-09-05"
    known_injuries = {
        "Chiefs": [], 
        "Ravens": ["Kyle Hamilton"] # Testing a star injury
    }
    
    result = forge.get_gamified_prediction("Chiefs", "Ravens", start_date, known_injuries)
    print(result)
