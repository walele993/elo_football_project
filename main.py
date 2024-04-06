from extract_match_info import extract_match_info
from utilities import extract_season_links, print_team_rankings, print_match_results, get_matches, craziest_match, print_season_team_rankings, print_hall_of_fame, get_team_position_in_season, best_teams_by_elo_increase, worst_teams_by_elo_increase
from elo_rating import EloRating
from plots import plot_ranking_evolution
import re

def main():
    # URL of the Serie A main page
    serie_a_url = "https://it.wikipedia.org/wiki/Serie_A"

    # Extract season links from the Serie A main page
    links = extract_season_links(serie_a_url)

    elo_rating = EloRating()

    # CSS selectors for tables
    selectors_both = [
        "#mw-content-text > div.mw-content-ltr.mw-parser-output > table.nowrap tbody",
        "#mw-content-text > div.mw-content-ltr.mw-parser-output > table:nth-child(68) tbody"
    ]

    # Extract match information from the current season
    for link in links:
        # Use a regular expression to find the year in the URL
        match = re.search(r'\d{4}', link)
        if match:
            current_season = int(match.group())
            extract_match_info(link, selectors_both, elo_rating, current_season)
            
    print_team_rankings(elo_rating)
      
if __name__ == "__main__":
    main()