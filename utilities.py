import requests
from bs4 import BeautifulSoup

def extract_season_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    selector_row_6 = "#navbox-Serie_A_storico > tbody > tr:nth-child(6)"
    selector_row_8 = "#navbox-Serie_A_storico > tbody > tr:nth-child(8)"

    row_6 = soup.select_one(selector_row_6)
    row_8 = soup.select_one(selector_row_8)

    if row_6 is None or row_8 is None:
        print(f"No elements found for {url}")
        return []

    season_links = []

    for link in row_6.find_all('a', href=True):
        season_links.append(link['href'])

    for link in row_8.find_all('a', href=True):
        season_links.append(link['href'])

    return season_links

def print_team_rankings(elo_rating):
    print("\nCurrent Standings:\n")
    sorted_teams = sorted(elo_rating.team_ratings.items(), key=lambda x: x[1], reverse=True)
    for team, rating in sorted_teams:
        best_record = elo_rating.best_elo.get(team, {})
        best_rating = best_record.get('rating', rating)
        best_matchday = best_record.get('matchday', "N/A")
        best_season = best_record.get('season', "N/A")
        print(f"{team}: {rating} (Best Elo: {best_rating} achieved on matchday {best_matchday} of season {best_season})")
        
def print_match_results(home_team, away_team, initial_rating_home, initial_rating_away, home_goals, away_goals, new_rating_home, new_rating_away, matchday, season):
    print(f"Matchday: {matchday} - Season: {season}")
    print(f"{home_team} ({initial_rating_home}) - {away_team} ({initial_rating_away}) Result: {home_goals}-{away_goals}")
    print(f"{home_team} Elo Change: {new_rating_home - initial_rating_home} (New Elo: {new_rating_home})")
    print(f"{away_team} Elo Change: {new_rating_away - initial_rating_away} (New Elo: {new_rating_away})\n")
    
def get_matches(elo_rating, *args):
    if len(args) == 1 and isinstance(args[0], str):
        # Search by team name
        matches = [match_info for match_info in elo_rating.match_history if args[0] in (match_info['home_team'], match_info['away_team'])]
    elif len(args) == 1 and isinstance(args[0], int):
        # Search by season
        matches = [match_info for match_info in elo_rating.match_history if match_info['season'] == args[0]]
    elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], int):
        # Search by team and season
        matches = [match_info for match_info in elo_rating.match_history if (args[0] in (match_info['home_team'], match_info['away_team'])) and match_info['season'] == args[1]]
    elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
        # Search by season and matchday
        matches = [match_info for match_info in elo_rating.match_history if match_info['season'] == args[0] and str(match_info['matchday']) == str(args[1])]
    elif len(args) == 3 and isinstance(args[0], str) and all(isinstance(arg, int) for arg in args[1:]):
        # Search by team, season, and matchday
        matches = [match_info for match_info in elo_rating.match_history if (args[0] in (match_info['home_team'], match_info['away_team'])) and match_info['season'] == args[1] and str(match_info['matchday']) == str(args[2])]
    else:
        raise ValueError("Invalid arguments")
    # Print match results
    for match in matches:
        print_match_results(match['home_team'], match['away_team'], match['initial_rating_home'], match['initial_rating_away'], match['home_goals'], match['away_goals'], match['new_rating_home'], match['new_rating_away'], match['matchday'], match['season'])

def craziest_match(elo_rating, num_matches):
    # Sort matches based on Elo score difference
    sorted_matches = sorted(elo_rating.match_history, key=lambda x: abs(x['new_rating_home'] - x['initial_rating_home']), reverse=True)
    for i in range(min(num_matches, len(sorted_matches))):
        match = sorted_matches[i]
        home_team = match['home_team']
        away_team = match['away_team']
        initial_rating_home = match['initial_rating_home']
        initial_rating_away = match['initial_rating_away']
        new_rating_home = match['new_rating_home']
        new_rating_away = match['new_rating_away']
        matchday = match['matchday']
        season = match['season']

        print_match_results(home_team, away_team, initial_rating_home, initial_rating_away, match['home_goals'], match['away_goals'], new_rating_home, new_rating_away, matchday, season)
        
def print_season_team_rankings(elo_rating, season):
    print(f"\nStandings for season {season}:\n")
    
    # Load standings from memory if already computed
    if season in elo_rating.season_standings:
        season_standings = elo_rating.season_standings[season]
    else:
        # Compute standings if not yet calculated
        season_standings = elo_rating.update_season_standings(season)
    
    # Print team standings for the specified season
    previous_season = season - 1
    
    for team, rating in season_standings.items():
        previous_season_used = None
        current_season = previous_season
        
        # Search for team's rating in the previous season
        while current_season >= 0 and previous_season_used is None:
            previous_rating = elo_rating.season_standings.get(current_season, {}).get(team)
            if previous_rating is not None:
                previous_season_used = current_season
            current_season -= 1
        
        # Calculate Elo score difference
        if previous_season_used is not None:
            rating_diff = rating - previous_rating
            print(f"{team}: {rating} ({'+' if rating_diff >= 0 else ''}{rating_diff})")
        else:
            # If previous rating is not available, consider initial rating as 1500
            print(f"{team}: {rating} ({rating - 1500})")
            
def print_hall_of_fame(elo_rating):
    champions_count = {}
    for season, champion in elo_rating.champions.items():
        champions_count[champion] = champions_count.get(champion, []) + [season]

    sorted_champions = sorted(champions_count.items(), key=lambda x: len(x[1]), reverse=True)
    
    print("Hall of Fame:\n")
    for champion, seasons in sorted_champions:
        print(f"{champion}: {len(seasons)} times ({', '.join(map(str, seasons))})")
        
def get_team_position_in_season(elo_rating, team, season=None):
    if season:
        if season not in elo_rating.season_standings:
            print(f"Season {season} does not yet have a calculated standings.")
            return

        season_standings = elo_rating.season_standings[season]

        # Find team's position in the standings of the specified season
        team_position = None
        for i, (team_name, elo) in enumerate(season_standings.items(), start=1):
            if team_name == team:
                team_position = i
                break

        if team_position is not None:
            print(f"{season}\n{team_position}. {team} ({elo})")
        else:
            print(f"{team} is not present in the standings of season {season}.")
    else:
        for season, season_standings in elo_rating.season_standings.items():
            team_position = None
            for i, (team_name, elo) in enumerate(season_standings.items(), start=1):
                if team_name == team:
                    team_position = i
                    break

            if team_position is not None:
                print(f"{season}\n{team_position}. {team} ({elo})")
                
def best_teams_by_elo_increase(elo_rating, num_teams):
    # List to store all Elo increases in a single season
    all_increases = []

    # Compute Elo increase for each team in each season
    for season, standings in elo_rating.season_standings.items():
        if season > 0:
            prev_season = season - 1
            prev_standings = elo_rating.season_standings.get(prev_season, {})
            for team, rating in standings.items():
                prev_rating = None
                current_season = prev_season
                
                # Search for team's rating in previous seasons until found or reaches season 0
                while current_season >= 0 and prev_rating is None:
                    prev_rating = prev_standings.get(team, None)
                    if prev_rating is None:
                        prev_season = current_season - 1
                        prev_standings = elo_rating.season_standings.get(prev_season, {})
                    current_season -= 1

                if prev_rating is None:
                    prev_rating = 1500  # Consider initial rating 1500 if rating in previous season is not found
                    
                elo_increase = rating - prev_rating
                all_increases.append((team, elo_increase, season))

    # Find top x Elo increases in a single season
    top_increases = sorted(all_increases, key=lambda x: x[1], reverse=True)[:num_teams]

    # Print top Elo increases
    print(f"Top {num_teams} Elo Changes in a Single Season:")
    for team, increase, season in top_increases:
        print(f"{team}: +{increase} Elo Points (Season {season})")
        
def worst_teams_by_elo_increase(elo_rating, num_teams):
    # List to store all Elo increases in a single season
    all_increases = []

    # Compute Elo increase for each team in each season
    for season, standings in elo_rating.season_standings.items():
        if season > 0:
            prev_season = season - 1
            prev_standings = elo_rating.season_standings.get(prev_season, {})
            for team, rating in standings.items():
                prev_rating = None
                current_season = prev_season
                
                # Search for team's rating in previous seasons until found or reaches season 0
                while current_season >= 0 and prev_rating is None:
                    prev_rating = prev_standings.get(team, None)
                    if prev_rating is None:
                        prev_season = current_season - 1
                        prev_standings = elo_rating.season_standings.get(prev_season, {})
                    current_season -= 1

                if prev_rating is None:
                    prev_rating = 1500  # Consider initial rating 1500 if rating in previous season is not found
                    
                elo_increase = rating - prev_rating
                all_increases.append((team, elo_increase, season))

    # Find bottom x Elo increases in a single season
    bottom_increases = sorted(all_increases, key=lambda x: x[1])[:num_teams]

    # Print bottom Elo increases
    print(f"Worst {num_teams} Elo Changes in a Single Season:")
    for team, increase, season in bottom_increases:
        print(f"{team}: {increase} Elo Points (Season {season})")