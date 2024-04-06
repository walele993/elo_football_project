import re
import requests
from bs4 import BeautifulSoup

def extract_match_info(url, selectors, elo_rating, season):
    # Check if the URL starts with "http"
    if not url.startswith("http"):
        url = "https://it.wikipedia.org" + url

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize a list for sorted results
    schedule = []
    # Initialize a list for matchdays
    matchdays = {}

    # Count how many tables were found among the selectors
    found_tables = sum(1 for selector in selectors if soup.select_one(selector) and 'giornata' in soup.select_one(selector).get_text(strip=True).lower())

    # Use the first code block only if both selectors are found
    if found_tables == len(selectors):
        # Iterate through the selectors
        for selector in selectors:
            # Find the element using the selector
            table = soup.select_one(selector)

            # Check if the table is found and contains the word "giornata"
            if table and 'giornata' in table.get_text(strip=True).lower():
                # Initialize a list for results
                results = []

                # Find the rows of the table
                for row in table.find_all('tr'):
                    # Extract all columns with data
                    row_data = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
                    row_data = [data for data in row_data if not re.match(r'\d{1,2}[º°]?\s*\w{3}\.?\s*', data)]

                    # Add the data list only if it's not empty
                    if row_data and len(row_data) <= 5:
                        results.append(row_data)

                # Add tuples if they don't contain null values OR contain the word "giornata"
                schedule.extend((result[0], result[1]) for result in results if (len(result) >= 2 and result[0] and result[1]) or ('giornata' in result[1].lower()))

        # Iterate through the schedule and organize matchdays
        current_matchday = None
        for item in schedule:
            if 'giornata' in item[1].lower():
                # Extract only the numerical part from the matchday string using a regular expression
                match = re.search(r'\d+', item[1])
                if match:
                    current_matchday = match.group()
                    matchdays[current_matchday] = []
            elif current_matchday:
                # Remove values within square brackets
                match_info = [re.sub(r'\[.*?\]', '', info) for info in item[0].split('-') + item[1].split('-')]
                match_info = tuple(info.strip() for info in match_info)
                matchdays[current_matchday].append(match_info)
    
        for matchday, match_list in sorted(matchdays.items(), key=lambda x: int(re.search(r'\d+', x[0]).group())):
            for match in match_list:
                home_team, away_team, home_goals, away_goals = match
                # Update the Elo ratings of the teams
                new_rating_home, new_rating_away = elo_rating.update_team_ratings(home_team, away_team, home_goals, away_goals, matchday, season)
    
    else:
        # Otherwise, use the second code block
        # Update the CSS selector
        selector = "#mw-content-text > div.mw-content-ltr.mw-parser-output > table.nowrap tbody"

        # Find the element using the selector
        table = soup.select_one(selector)

        # Check if the table is found and contains the word "giornata"
        if table and 'giornata' in table.get_text(strip=True).lower():
            # Initialize a list for results
            results = []
            # Initialize a list for sorted results
            schedule = []
            # Initialize a list for matchdays
            matchdays = {}

            # Find the rows of the table
            for row in table.find_all('tr'):
                # Extract all columns with data
                row_data = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
                row_data = [data for data in row_data if not re.match(r'\d{1,2}[º°]?\s*\w{3}\.?\s*', data)]

                # Add the data list only if it's not empty
                if row_data and len(row_data) <= 5:
                    results.append(row_data)

            # Add tuples if they don't contain null values
            schedule.extend((result[1], result[0]) for result in results if len(result) >= 2 and result[0] and result[1])
            schedule.extend((result[1], result[2]) for result in results if len(result) >= 3 and result[1] and result[2])

            # Iterate through the schedule and organize matchdays
            current_matchday = None
            for item in schedule:
                if 'giornata' in item[0].lower():
                    # Extract only the numerical part from the matchday string using a regular expression
                    match = re.search(r'\d+', item[1])
                    if match:
                        current_matchday = match.group()
                        matchdays[current_matchday] = []
                elif current_matchday:
                    match_info = [re.sub(r'\[.*?\]', '', info) for info in item[0].split('-') + item[1].split('-')]
                    match_info = tuple(info.strip() for info in match_info)
                    matchdays[current_matchday].append(match_info)
        
            for matchday, match_list in sorted(matchdays.items(), key=lambda x: int(re.search(r'\d+', x[0]).group())):
                for match in match_list:
                    home_team, away_team, home_goals, away_goals = match
                    # Update the Elo ratings of the teams
                    new_rating_home, new_rating_away = elo_rating.update_team_ratings(home_team, away_team, home_goals, away_goals, matchday, season)
