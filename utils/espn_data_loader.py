"""ESPN Data Loader - Populates team_stats with win/loss records and point differentials"""
import requests
import sqlite3
from datetime import datetime
from .config import get_db_path, init_databases

ESPN_ENDPOINTS = {
    "NCAAB_STANDINGS": "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/standings",
    "NCAAB_SCOREBOARD": "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard"
}

def load_ncaab_standings():
    """Fetch NCAA Basketball standings from ESPN"""
    print("[ SCANNING ESPN NCAAB STANDINGS... ]")
    
    try:
        response = requests.get(ESPN_ENDPOINTS["NCAAB_STANDINGS"], timeout=10)
        response.raise_for_status()
        data = response.json()
        
        team_stats = {}
        
        for group in data.get('standings', {}).get('groups', []):
            for team in group.get('team', []):
                team_name = team.get('displayName', '')
                stats = team.get('stats', [])
                
                wins = 0
                losses = 0
                points_for = 0.0
                points_against = 0.0
                
                for stat in stats:
                    stat_name = stat.get('name', '')
                    stat_value = float(stat.get('value', 0))
                    
                    if stat_name == 'wins':
                        wins = int(stat_value)
                    elif stat_name == 'losses':
                        losses = int(stat_value)
                    elif stat_name == 'pointsFor':
                        points_for = stat_value
                    elif stat_name == 'pointsAgainst':
                        points_against = stat_value
                
                if team_name:
                    team_stats[team_name] = {
                        'wins': wins,
                        'losses': losses,
                        'points_for': points_for,
                        'points_against': points_against,
                        'differential': points_for - points_against
                    }
        
        return team_stats
    
    except Exception as e:
        print(f"[ ERROR LOADING STANDINGS: {e} ]")
        return {}

def load_ncaab_scores():
    """Fetch recent games from ESPN"""
    print("[ SCANNING ESPN NCAAB RECENT GAMES... ]")
    
    try:
        response = requests.get(ESPN_ENDPOINTS["NCAAB_SCOREBOARD"], timeout=10)
        response.raise_for_status()
        data = response.json()
        
        team_points = {}
        
        for event in data.get('events', []):
            if event.get('status', {}).get('type') != 'final':
                continue
            
            comp = event.get('competitions', [{}])[0]
            competitors = comp.get('competitors', [])
            
            if len(competitors) < 2:
                continue
            
            home_comp = competitors[0]
            away_comp = competitors[1]
            
            home_team = home_comp.get('team', {}).get('displayName', '')
            away_team = away_comp.get('team', {}).get('displayName', '')
            
            home_score = int(home_comp.get('score', 0))
            away_score = int(away_comp.get('score', 0))
            
            if home_team and away_team:
                if home_team not in team_points:
                    team_points[home_team] = {'for': 0, 'against': 0, 'games': 0}
                if away_team not in team_points:
                    team_points[away_team] = {'for': 0, 'against': 0, 'games': 0}
                
                team_points[home_team]['for'] += home_score
                team_points[home_team]['against'] += away_score
                team_points[home_team]['games'] += 1
                
                team_points[away_team]['for'] += away_score
                team_points[away_team]['against'] += home_score
                team_points[away_team]['games'] += 1
        
        return team_points
    
    except Exception as e:
        print(f"[ ERROR LOADING SCORES: {e} ]")
        return {}

def save_team_stats(standings_data, scores_data):
    """Save team stats to database"""
    conn = sqlite3.connect(str(get_db_path()))
    cursor = conn.cursor()
    
    all_teams = set(standings_data.keys()) | set(scores_data.keys())
    
    for team_name in all_teams:
        stands = standings_data.get(team_name, {})
        scores = scores_data.get(team_name, {})
        
        wins = stands.get('wins', 0)
        losses = stands.get('losses', 0)
        points_for = stands.get('points_for', 0) or (scores.get('for', 0) / max(scores.get('games', 1), 1))
        points_against = stands.get('points_against', 0) or (scores.get('against', 0) / max(scores.get('games', 1), 1))
        
        cursor.execute('''
            INSERT OR REPLACE INTO team_stats
            (team_name, wins, losses, points_for, points_against, last_updated)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (team_name, wins, losses, points_for, points_against))
    
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM team_stats")
    team_count = cursor.fetchone()[0]
    print(f"[ SUCCESS: {team_count} TEAMS CATALOGED IN MEMORY ]")
    
    cursor.execute('''
        SELECT team_name, wins, losses, ROUND(points_for - points_against, 1) as diff
        FROM team_stats
        ORDER BY diff DESC
        LIMIT 5
    ''')
    
    print("[ TOP DIFFERENTIALS ]")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}-{row[2]} ({row[3]:+.1f} pts)")
    
    conn.close()

def sync_all_data():
    """Main sync function"""
    print("\n" + "="*60)
    print("[ AI STRIKES - ARCHITECT MEMORY SYNC ]")
    print("="*60 + "\n")
    
    init_databases()
    
    standings = load_ncaab_standings()
    scores = load_ncaab_scores()
    
    if standings or scores:
        save_team_stats(standings, scores)
    else:
        print("[ WARNING: No data received from ESPN ]")
    
    print("\n[ ARCHITECT READY FOR STRIKES ]\n")

if __name__ == "__main__":
    sync_all_data()
