import matplotlib.pyplot as plt

def plot_ranking_evolution(elo_rating, highlight_team=None, specific_season=None):
    # Initialize a dictionary to store teams' Elo scores for each matchday
    ranking_evolution = {}

    # Calculate Elo scores at the end of the previous season
    last_season_final_scores = {}
    for season, season_data in elo_rating.season_standings.items():
        last_season = season - 1
        if last_season in elo_rating.season_standings:
            last_season_final_scores[season] = elo_rating.season_standings[last_season]

    # Iterate through the match history to build the ranking evolution
    for match_info in elo_rating.match_history:
        matchday = match_info['matchday']
        season = match_info['season']
        home_team = match_info['home_team']
        away_team = match_info['away_team']
        new_rating_home = match_info['new_rating_home']
        new_rating_away = match_info['new_rating_away']

        # Add teams' Elo scores to the ranking for the corresponding matchday
        if season not in ranking_evolution:
            ranking_evolution[season] = {}

        if matchday not in ranking_evolution[season]:
            ranking_evolution[season][matchday] = {}

        ranking_evolution[season][matchday][home_team] = new_rating_home
        ranking_evolution[season][matchday][away_team] = new_rating_away

    # Create the plot with different sizes based on the specified season
    if specific_season:
        fig, ax = plt.subplots(figsize=(30, 20))
    else:
        fig, ax = plt.subplots(figsize=(300, 20))

    # Iterate through teams to create a line for each
    for team, _ in sorted(elo_rating.team_ratings.items(), key=lambda x: x[1], reverse=True):
        # Initialize lists for x (matchdays) and y (Elo scores) values of the current team
        x_values = []
        y_values = []

        # Iterate through seasons and matchdays to gather the team's Elo scores
        total_matchdays_passed = 0  # Variable to keep track of the total passed matchdays
        season_ticks = []  # List to store the starts of the seasons
        for season, season_data in ranking_evolution.items():
            if specific_season is not None and season != specific_season:
                continue  # Skip unwanted seasons
            
            x_values_season = []  # List for matchdays of the season
            y_values_season = []  # List for Elo scores of the season

            # Get Elo scores at the end of the previous season
            if season > 0 and season - 1 in last_season_final_scores:
                last_season_scores = last_season_final_scores[season]
                if team in last_season_scores:
                    x_values_season.append(total_matchdays_passed)  # Day 0 of the current season
                    y_values_season.append(last_season_scores[team])

            for matchday, matchday_data in sorted(season_data.items(), key=lambda x: int(x[0])):
                # Calculate the actual matchday including matchdays of previous seasons
                actual_matchday = total_matchdays_passed + int(matchday)
                
                # If the team played on that matchday, add the Elo score, otherwise None
                if team in matchday_data:
                    x_values_season.append(actual_matchday)
                    y_values_season.append(matchday_data[team])
                else:
                    x_values_season.append(actual_matchday)
                    y_values_season.append(None)
        
            # Add the coordinates of the current season to the team's general coordinates
            x_values.extend(x_values_season)
            y_values.extend(y_values_season)
        
            # Update the total passed matchdays
            total_matchdays_passed += len(season_data)
        
            # Add a light gray vertical line at the beginning of each season
            if not specific_season:
                season_ticks.append(total_matchdays_passed)
                ax.axvline(x=total_matchdays_passed, color='lightgrey', linestyle='--', linewidth=1)
        
        # Set the x-axis limit based on the maximum matchdays for a single season or 40 matchdays for a season
        if specific_season:
            max_matchdays = max(len(season_data) for season_data in ranking_evolution[specific_season].values())
            ax.set_xlim(0, max_matchdays)  # Set the limit to 40 matchdays for a single season
        else:
            max_matchdays = max(len(season_data) for season_data in ranking_evolution.values())
            ax.set_xlim(0, total_matchdays_passed + max_matchdays)  # Set the limit to the maximum across all seasons

        if highlight_team:
            if team == highlight_team:
                ax.plot(x_values, y_values, marker='o', label=team, color='blue', linewidth=2.5)
            else:
                ax.plot(x_values, y_values, marker='o', label=team, color='lightgrey', zorder=1)
        else:
            ax.plot(x_values, y_values, marker='o', label=team)

        # Add a label at the end of the line with the same color as the line
        if y_values[-1] is not None:
            ax.annotate(team, (x_values[-1], y_values[-1]), textcoords="offset points", xytext=(10,0), ha='left', color=ax.lines[-1].get_color())

    # Set titles and axis labels
    if highlight_team and specific_season:
        filename = f"elo_ranking_{highlight_team}_{specific_season}.png"
        ax.set_title(f'Elo Score Evolution of {highlight_team} in Season {specific_season}')
    elif specific_season is not None:
        filename = f"elo_ranking_{specific_season}_season.png"
        ax.set_title(f'Elo Score Evolution of Teams in Season {specific_season}')
    elif highlight_team:
        filename = f"elo_ranking_{highlight_team}.png"
        ax.set_title(f'Elo Score Evolution of {highlight_team} Over Time')
    else:
        filename = "elo_ranking.png"
        ax.set_title('Elo Score Evolution of Teams Over Time')

    ax.set_xlabel('Season' if not specific_season else 'Matchday')
    ax.set_ylabel('Elo Score')
    
    # Set ticks on the x-axis as the start of each season
    ax.set_xticks(season_ticks if not specific_season else range(0, total_matchdays_passed + 1))
    # Add labels to indicate the corresponding season
    ax.set_xticklabels([f'{season-1}-{season}' for season in ranking_evolution.keys()] if not specific_season else range(0, total_matchdays_passed + 1), rotation=45, ha='right')

    # Hide right and top axes
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Color axes and labels
    ax.tick_params(axis='x', colors='dimgray')
    ax.tick_params(axis='y', colors='dimgray')
    
    # Save the plot as an image file
    plt.savefig(filename)
    plt.close(fig)