class EloRating:
    def __init__(self):
        self.team_ratings = {}
        self.best_elo = {}
        self.match_history = []  # History of matches
        self.matchdays = {}  # Match schedule divided by matchdays
        self.season_standings = {}  # Standings for seasons
        self.champions = {}  # Champions for each season

    def get_team_rating(self, team):
        return self.team_ratings.get(team, 1500)

    def update_team_ratings(self, home_team, away_team, home_goals, away_goals, matchday, season):
        k_factor = 32
    
        rating_home = self.get_team_rating(home_team)
        rating_away = self.get_team_rating(away_team)
        
        result = 1 if home_goals > away_goals else 0.5 if home_goals == away_goals else 0
        
        expected_score_home = 1 / (1 + 10 ** ((rating_away - rating_home) / 400))
        expected_score_away = 1 / (1 + 10 ** ((rating_home - rating_away) / 400))
        
        new_rating_home = int(round(rating_home + k_factor * (result - expected_score_home)))
        new_rating_away = int(round(rating_away + k_factor * ((1 - result) - expected_score_away)))
        
        self.team_ratings[home_team] = new_rating_home
        self.team_ratings[away_team] = new_rating_away
        
        # Update best records only if new Elo scores are better than the previous ones
        if new_rating_home > self.best_elo.get(home_team, {}).get('rating', float('-inf')):
            self.best_elo[home_team] = {'rating': new_rating_home,
                                        'matchday': matchday,
                                        'season': season + 1}
        if new_rating_away > self.best_elo.get(away_team, {}).get('rating', float('-inf')):
            self.best_elo[away_team] = {'rating': new_rating_away,
                                        'matchday': matchday,
                                        'season': season + 1}

        # Add match information to the match history
        match_info = {
            'home_team': home_team,
            'away_team': away_team,
            'initial_rating_home': rating_home,
            'initial_rating_away': rating_away,
            'home_goals': home_goals,
            'away_goals': away_goals,
            'new_rating_home': new_rating_home,
            'new_rating_away': new_rating_away,
            'matchday': matchday,
            'season': season + 1
        }
        self.match_history.append(match_info)
        
        # Call to update season standings
        self.update_season_standings(season + 1)

        return new_rating_home, new_rating_away
        
    def update_season_standings(self, season):
        # Calculate standings for the specified season and save it in the dictionary of season standings
        season_teams = set()
        season_ratings = {}
        for match_info in self.match_history:
            if match_info['season'] == season:
                home_team = match_info['home_team']
                away_team = match_info['away_team']
                season_teams.add(home_team)
                season_teams.add(away_team)
                season_ratings[home_team] = self.team_ratings.get(home_team, 1500)
                season_ratings[away_team] = self.team_ratings.get(away_team, 1500)
    
        sorted_teams = sorted(season_ratings.items(), key=lambda x: x[1], reverse=True)
        season_standings = {team: rating for team, rating in sorted_teams}
        self.season_standings[season] = season_standings
        
        champion = next(iter(sorted_teams))[0]  # The team with the highest Elo score
        self.champions[season] = champion