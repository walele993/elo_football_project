# Elo Rating System for Football Leagues

## Program Description

This program is designed to extract and analyze match data from Wikipedia pages related to Serie A, the top professional football league in Italy. It utilizes Elo ratings to evaluate and track the performance of football teams across different seasons.

## Dependencies

The program relies on the following dependencies:
- Python 3.x
- BeautifulSoup4
- Requests
- Matplotlib
- Re

## Usage Instructions

To use the program, follow these steps:
1. Ensure you have Python 3.x installed on your system.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run the main script `main.py` to extract and analyze Serie A match data.

## Elo Rating Explanation

The Elo rating system, developed by Arpad Elo, is primarily known for assessing the relative skill levels of players in two-player games, such as chess. However, it has been adapted for use in football to evaluate and rank teams based on their performance. The main objective of the Elo rating system in football is to provide an objective measure of team performance and use it to classify teams according to their relative strength.

The formula used to update Elo ratings after each match is as follows: `R' = R + K * (S - E)`

Where:
- R' is the new Elo rating
- R is the previous Elo rating
- K is the K-factor, determining the sensitivity of the rating update
- S is the actual result of the match (1 for win, 0.5 for draw, 0 for loss)
- E is the expected result of the match, calculated using the teams' Elo ratings

In practice, the greater the difference between the actual result `S` and the expected result `E`, the larger the update to the rating `R`. For example, if a winning team has a lower rating than expected, its rating will increase more significantly compared to an expected victory. This system allows for the adjustment of team ratings based on their actual performances, ensuring a more accurate and dynamic ranking over time.

It's worth noting that while the Elo rating system is well-established in other competitive domains like chess, its application in football, as you've implemented in your code, is less common but can be a valuable tool for assessing team performance and making informed decisions in the context of the sport.

## Key Features

#### 1. Extracting Season Links

- **Function:** `extract_season_links(url)`
- **Description:** Extracts links to Serie A season pages from Wikipedia.
- **Usage:** Pass the URL of the Serie A main page as an argument.

#### 2. Extracting Match Information

- **Function:** `extract_match_info(url, selectors, elo_rating, season)`
- **Description:** Extracts match information such as teams, scores, and Elo ratings from Wikipedia pages.
- **Usage:** Pass the Wikipedia URL, CSS selectors, Elo rating object, and season as arguments.

#### 3. Updating Elo Ratings

- **Class:** `EloRating`
- **Description:** Implements the Elo rating system to update and maintain team ratings.
- **Methods:**
  - `get_team_rating(team)`: Get the Elo rating of a specific team.
  - `update_team_ratings(home_team, away_team, home_goals, away_goals, matchday, season)`: Update Elo ratings based on match results.
  - `update_season_standings(season)`: Update standings for the specified season.

#### 4. Printing Team Rankings

- **Function:** `print_team_rankings(elo_rating)`
- **Description:** Prints the current Elo ratings and the best Elo ratings achieved by each team.
- **Usage:** Pass the Elo rating object as an argument.

#### 5. Printing Match Results

- **Function:** `print_match_results(home_team, away_team, initial_rating_home, initial_rating_away, home_goals, away_goals, new_rating_home, new_rating_away, matchday, season)`
- **Description:** Prints the results of a single match, including Elo rating changes.
- **Usage:** Pass match details as arguments.

#### 6. Getting Matches

- **Function:** `get_matches(elo_rating, *args)`
- **Description:** Retrieves match information based on different search criteria.
- **Usage:** Provide search criteria such as team name, season, or both as arguments.

#### 7. Finding the Craziest Match

- **Function:** `craziest_match(elo_rating, num_matches)`
- **Description:** Identifies the craziest matches based on the largest Elo rating changes.
- **Usage:** Specify the number of craziest matches to display.

#### 8. Printing Season Team Rankings

- **Function:** `print_season_team_rankings(elo_rating, season)`
- **Description:** Prints team rankings for a specific season.
- **Usage:** Pass the Elo rating object and the season as arguments.

#### 9. Printing Hall of Fame

- **Function:** `print_hall_of_fame(elo_rating)`
- **Description:** Prints the champions and their titles in the Hall of Fame.
- **Usage:** Pass the Elo rating object as an argument.

#### 10. Getting Team Position in Season

- **Function:** `get_team_position_in_season(elo_rating, team, season=None)`
- **Description:** Retrieves the position of a team in the standings for a specific season.
- **Usage:** Pass the Elo rating object, team name, and optionally the season as arguments.

#### 11. Finding Best Teams by Elo Increase

- **Function:** `best_teams_by_elo_increase(elo_rating, num_teams)`
- **Description:** Identifies the teams with the highest Elo increases in a single season.
- **Usage:** Specify the number of teams to display.

#### 12. Finding Worst Teams by Elo Increase

- **Function:** `worst_teams_by_elo_increase(elo_rating, num_teams)`
- **Description:** Identifies the teams with the lowest Elo increases in a single season.
- **Usage:** Specify the number of teams to display.

#### 13. Plotting Ranking Evolution

- **Function:** `plot_ranking_evolution(elo_rating, highlight_team=None, specific_season=None)`
- **Description:** Generates a plot showing the evolution of Elo ratings over time.
- **Usage:** Pass the Elo rating object, and optionally a team name or specific season to highlight.

## Additional Notes

- The `results` file will contain data regarding the current standings, the hall of fame, the most memorable matches of all time, and the best seasons in terms of Elo ratings for individual teams.
- This is my first programming project, and I welcome feedback, pull requests, and suggestions for improvement.
- The data is sourced from Wikipedia and may contain errors.
- Future updates may include support for other leagues, sports, or additional analytical features.

## Credits

This project was created by Gabriele Meucci.
