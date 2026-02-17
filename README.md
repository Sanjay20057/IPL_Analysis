# 🏏 IPL Analysis Dashboard — Streamlit App

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-yellow?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red?style=for-the-badge&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=for-the-badge&logo=plotly)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**An interactive IPL (Indian Premier League) analytics dashboard built with Streamlit. Explore team performance, batsman and bowler stats, boundary analysis, and Orange Cap holders across IPL seasons 2008–2019.**

[Features](#-features) · [Modules](#-modules) · [Installation](#-installation) · [Usage](#-usage) · [Dataset](#-dataset) · [Project Structure](#-project-structure)

</div>

---

## ✨ Features

- 📊 **7 analysis modules** accessible from the sidebar
- 🎯 **Filterable views** — drill down by team, player, season, or boundary type
- 📈 **Rich visualizations** using both Matplotlib and Plotly (bar, line, pie, area, scatter, histogram)
- 🏆 **Season winners** and win count comparisons across all IPL franchises
- 🦾 **Orange Cap tracker** — top run-scorer per season, visualized with a scatter plot
- 🏏 **Per-batsman breakdown** — runs scored against each bowling team
- 🎳 **Bowler analysis** — total runs conceded with pie and line charts
- 🔴 **Boundary analysis** — fours and sixes comparison with dual-line overlay chart

---

## 📋 Modules

### 1. 🏟️ Most Played Team
- Ranks all IPL teams by total matches played
- Displays results in a sortable table
- Visualized with a Matplotlib line chart and an interactive Plotly line chart

### 2. 🏆 Season Winner
- Filter by **season** and/or **winning team** using sidebar dropdowns
- Shows the IPL winner for each season in a bar chart
- Displays total number of IPL title wins per team in a second bar chart

### 3. 🏏 Batsman
- Filter to a specific batsman or view the **Overall Top 25**
- Total runs scored across IPL seasons 2008–2019
- Vertical and horizontal bar charts for easy comparison

### 4. 🎳 Bowler
- Filter to a specific bowler or view the **Overall Top 25**
- Total runs conceded across seasons
- Plotly line chart and pie chart showing run distribution among top 25 bowlers

### 5. 🔴 Boundaries Analysis
- Filter by **run type** (4 or 6) and **batsman**
- Histogram of fours hit by all batsmen
- Area chart of top 25 six-hitters
- Dual-line overlay chart comparing fours vs. sixes for top batsmen

### 6. 📊 Batsman Score
- Select any batsman to see their **runs against each bowling team**
- Table + Plotly chart rendered from the `helper.batsman_scored()` function

### 7. 🟠 Orange Cap Holder
- Filter by season or view all seasons at once
- Table of Orange Cap winners per season
- Scatter plot with encoded Y-axis showing which batsman won the Orange Cap in each season

---

## 📂 Project Structure

```
ipl-analysis/
│
├── app.py                      # Main Streamlit dashboard
├── helper.py                   # All data processing & chart helper functions
│
├── IPL-anaylsis/
│   ├── deliveries(1).csv       # Ball-by-ball delivery data
│   └── matches(1).csv          # Match-level data (teams, venue, winner, season)
│
└── requirements.txt            # Python dependencies
```

### `helper.py` Functions

| Function | Description |
|---|---|
| `Most_Played_Team(Matches)` | Count matches played per team |
| `Season_Winner(Matches)` | Extract unique seasons and winners for dropdowns |
| `fetch_Season_Winner(Matches, season, winner)` | Filter season winner data |
| `Batsman_Run(Deliveries)` | Get list of batsmen for dropdown |
| `fetch_Batsman_Run(Deliveries, batsman)` | Fetch runs for a selected batsman |
| `Bolwer_Run(Deliveries)` | Get list of bowlers for dropdown |
| `fetch_Bowler_Run(Deliveries, bowler)` | Fetch runs conceded by a selected bowler |
| `boundry(Deliveries)` | Get boundary run types and batsmen for dropdowns |
| `count_boundaries(Deliveries, run, batsman)` | Filter boundary data |
| `batsman(Deliveries)` | Get all batsman names |
| `batsman_scored(Deliveries, name)` | Return a Plotly chart for a batsman's runs vs teams |
| `season(Matches)` | Get all seasons for dropdown |
| `orange_cap_holder(Deliveries, Matches, season)` | Find Orange Cap winner per season |

---

## ⚙️ Installation

### Prerequisites
- Python 3.9 or higher

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ipl-analysis.git
cd ipl-analysis
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

1. Use the **sidebar radio menu** to select an analysis module
2. Use the **sidebar dropdowns** to filter by team, player, or season
3. View interactive Plotly charts and data tables in the main panel

---

## 🗄️ Dataset

The app uses two CSV files covering IPL seasons **2008–2019**:

### `deliveries(1).csv` — Ball-by-Ball Data

| Column | Description |
|---|---|
| `match_id` | Unique match identifier |
| `batsman` | Batsman on strike |
| `bowler` | Bowler delivering the ball |
| `batsman_runs` | Runs scored by the batsman off that ball |
| `total_runs` | Total runs off that ball (including extras) |
| `bowling_team` | Team bowling |

### `matches(1).csv` — Match-Level Data

| Column | Description |
|---|---|
| `id` | Unique match identifier |
| `season` | IPL season year |
| `team1` | Home team |
| `team2` | Away team |
| `winner` | Winning team |

> **Data source:** [Kaggle — IPL Dataset](https://www.kaggle.com/datasets/manasgarg/ipl)

---

## 📦 Dependencies

```
streamlit
pandas
matplotlib
plotly
```

Install all at once:

```bash
pip install streamlit pandas matplotlib plotly
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

*Built with ❤️ using Streamlit · Plotly · Pandas · IPL Dataset 2008–2019*

</div>
