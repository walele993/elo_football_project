# ⚽ Elo Rating System for Football Leagues

*Track team performance over time with an advanced Elo rating system!*  

---

## 🚀 Introduction

**Elo Rating System for Football Leagues** is a Python-based tool that extracts and analyzes match data from Wikipedia pages, applying an **Elo rating system** to evaluate and rank teams over multiple seasons. Designed for **Serie A**, this project offers deep insights into team performances and historical trends.

### Key Features
- 🏆 **Dynamic Elo Ratings**: Track and update team ratings after every match.
- 📈 **Performance Analysis**: Identify the best and worst teams by Elo progression.
- 🌍 **Web Scraping Automation**: Extract match data directly from Wikipedia.
- 📅 **Historical Data**: View season standings, hall of fame, and ranking evolution.
- 🎨 **Data Visualization**: Generate insightful plots of team rankings over time.

---

## 🛋️ Installation

### Prerequisites
- Python 3.x
- SQLite (built-in with Python)

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

1. **Extract & Analyze Data**:  
   Run the main script to extract match results and compute Elo ratings:
   ```bash
   python main.py
   ```

2. **View Team Rankings**:  
   ```bash
   python main.py --rankings
   ```

3. **Analyze a Specific Season**:  
   ```bash
   python main.py --season 2023
   ```

4. **Find the Craziest Matches (Biggest Elo Changes)**:  
   ```bash
   python main.py --craziest 5
   ```

5. **Visualize Elo Evolution**:  
   ```bash
   python main.py --plot
   ```

---

## 🧠 How Elo Ratings Work

The **Elo rating system**, originally developed for chess, has been adapted for football to measure team strength. Each match influences the teams' ratings based on performance expectations.

**Formula:**
```math
R' = R + K * (S - E)
```
Where:
- `R'` = new rating
- `R` = current rating
- `K` = sensitivity factor (adjusts rating impact)
- `S` = actual result (1 = win, 0.5 = draw, 0 = loss)
- `E` = expected result based on pre-match ratings

Teams gain or lose points depending on match results, with **upsets** leading to more dramatic rating shifts!

---

## 📝 Key Functions

### ✨ Data Extraction & Processing
- **`extract_season_links(url)`** → Scrapes Wikipedia for season pages.
- **`extract_match_info(url, selectors, elo_rating, season)`** → Retrieves match results and updates Elo ratings.

### 🏋️‍♂️ Elo Rating Management
- **`get_team_rating(team)`** → Retrieve a team’s Elo rating.
- **`update_team_ratings(home_team, away_team, home_goals, away_goals, matchday, season)`** → Compute Elo adjustments.
- **`update_season_standings(season)`** → Refresh season rankings.

### 📊 Data Analysis & Visualization
- **`print_team_rankings(elo_rating)`** → Display current team rankings.
- **`craziest_match(elo_rating, num_matches)`** → Identify matches with the largest Elo swings.
- **`plot_ranking_evolution(elo_rating, highlight_team, specific_season)`** → Generate team ranking trend graphs.

---

## 🎨 Data Visualization

This tool includes a powerful **graphing feature** using Matplotlib! Track ranking evolution over time with:

```bash
python main.py --plot
```

Example Output:
- 🔼 Teams that surged up the rankings.
- 🔽 Teams that struggled across seasons.
- 📅 Significant historical shifts in Serie A power dynamics.

---

## 💪 Future Enhancements

- 🌐 Expand support for other leagues (Premier League, La Liga, Bundesliga).
- 📝 Include player performance metrics.
- 👁️ More advanced visualizations (heatmaps, comparative graphs).
- 🚀 Web dashboard for real-time tracking.

---

## 🏅 Contribution

This is my **first programming project**, and I'd love your feedback!  

1. **Fork** the repository  
2. **Clone** your fork:  
   ```bash
   git clone https://github.com/your-username/elo-football.git
   ```
3. Create a **feature branch**:  
   ```bash
   git checkout -b feature-enhancement
   ```
4. **Push** changes & submit a **pull request**

---

## 🏁 Credits

Project created by **Gabriele Meucci**.  

Data sourced from **Wikipedia**, which may contain occasional inaccuracies.

---

*Ready to analyze football like never before? Let’s go!* ⚽🔥

