import os, sqlite3, pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "database.sqlite"
EXPORTS = DATA_DIR / "exports"
TEXTDIR = DATA_DIR / "text"
EXPORTS.mkdir(exist_ok=True, parents=True)
TEXTDIR.mkdir(exist_ok=True, parents=True)

assert DB_PATH.exists(), f"DB not found at {DB_PATH}"

con = sqlite3.connect(DB_PATH)

# 0) Ülkeler & ligler
countries = pd.read_sql("SELECT id, name FROM Country", con)
countries = countries.rename(columns={"id": "country_id", "name": "country_name"})

leagues = pd.read_sql(
    "SELECT id as league_id, country_id, name as league_name FROM League", con
)

# SAĞLAM MERGE: country_id ile birleştir -> country_name garantili
leagues_full = leagues.merge(countries, on="country_id", how="left")

print("Available countries:", countries["country_name"].unique().tolist())
print("\nSample leagues (first 20):")
print(leagues_full.head(20)[["league_id", "country_name", "league_name"]])

# ---- Dataset'te kesin bulunan ülkelerden seçelim
TARGET_COUNTRIES = ["England", "Spain", "Germany", "Italy", "France", "Portugal", "Netherlands", "Belgium"]
target_league_ids = leagues_full[leagues_full["country_name"].isin(TARGET_COUNTRIES)]["league_id"].tolist()
print("\nTarget league ids:", target_league_ids[:10], "... total:", len(target_league_ids))
if not target_league_ids:
    raise SystemExit("No leagues matched TARGET_COUNTRIES. Pick other countries from the printed list.")

# 1) Takımlar
teams = pd.read_sql("SELECT team_api_id, team_long_name, team_short_name FROM Team", con)

# 2) Maçlar (seçilen ligler)
matches = pd.read_sql(f"""
SELECT m.id, m.season, m.date,
       m.home_team_api_id, m.away_team_api_id,
       m.home_team_goal, m.away_team_goal,
       m.league_id
FROM Match m
WHERE m.league_id IN ({",".join(map(str, target_league_ids))})
""", con, parse_dates=["date"])

# Takım isimleri
matches = (
    matches.merge(teams, left_on="home_team_api_id", right_on="team_api_id", how="left")
           .rename(columns={"team_long_name": "home_team_name"})
           .drop(columns=["team_api_id", "team_short_name"])
)
matches = (
    matches.merge(teams, left_on="away_team_api_id", right_on="team_api_id", how="left")
           .rename(columns={"team_long_name": "away_team_name"})
           .drop(columns=["team_api_id", "team_short_name"])
)

def season_start_year(s):
    try:
        return int(str(s).split("/")[0])
    except Exception:
        return None

matches["season_year"] = matches["season"].apply(season_start_year)

# 3) CSV dışa aktar
matches.to_csv(EXPORTS / "matches_selected_leagues.csv", index=False, encoding="utf-8")
teams.to_csv(EXPORTS / "teams.csv", index=False, encoding="utf-8")
leagues_full.to_csv(EXPORTS / "leagues_full.csv", index=False, encoding="utf-8")
print("\nExports written to", EXPORTS)

# 4) Özet üretim (örnek popüler takımlar)
TEAMS_OF_INTEREST = [
    # England
    "Manchester United", "Manchester City", "Liverpool", "Chelsea", "Arsenal", "Tottenham Hotspur",
    # Spain
    "Real Madrid", "FC Barcelona", "Atlético Madrid",
    # Germany
    "Bayern Munich", "Borussia Dortmund",
    # Italy
    "Juventus", "Inter", "AC Milan",
    # France
    "Paris Saint-Germain"
]
years = sorted(matches["season_year"].dropna().unique())

def write_team_year_summary(df, team_name, year):
    sub = df[((df["home_team_name"] == team_name) | (df["away_team_name"] == team_name)) & (df["season_year"] == year)]
    if sub.empty:
        return
    played = len(sub)
    gf = int((sub.query("home_team_name == @team_name")["home_team_goal"].sum() or 0) +
             (sub.query("away_team_name == @team_name")["away_team_goal"].sum() or 0))
    ga = int((sub.query("home_team_name == @team_name")["away_team_goal"].sum() or 0) +
             (sub.query("away_team_name == @team_name")["home_team_goal"].sum() or 0))

    def result(row):
        if row["home_team_name"] == team_name:
            if row["home_team_goal"] > row["away_team_goal"]:
                return "W"
            if row["home_team_goal"] < row["away_team_goal"]:
                return "L"
            return "D"
        else:
            if row["away_team_goal"] > row["home_team_goal"]:
                return "W"
            if row["away_team_goal"] < row["home_team_goal"]:
                return "L"
            return "D"

    res = sub.apply(result, axis=1)
    wins, draws, losses = int((res == "W").sum()), int((res == "D").sum()), int((res == "L").sum())

    away = sub.query("away_team_name == @team_name")
    away_wins = int((away["away_team_goal"] > away["home_team_goal"]).sum()) if not away.empty else 0

    lines = []
    lines.append(f"# {team_name} – Season {year}")
    lines.append(f"- Matches: {played}")
    lines.append(f"- Goals: {gf} for, {ga} against")
    lines.append(f"- Record (W/D/L): {wins}/{draws}/{losses}")
    lines.append(f"- Away wins: {away_wins}")
    lines.append("## Match list")
    for _, r in sub.sort_values("date").iterrows():
        lines.append(f"- {r['date'].date()} | {r['home_team_name']} {r['home_team_goal']}–{r['away_team_goal']} {r['away_team_name']}")
    text = "\n".join(lines)
    (TEXTDIR / f"{team_name.replace(' ', '_')}_{year}.md").write_text(text, encoding="utf-8")

for t in TEAMS_OF_INTEREST:
    for y in years:
        write_team_year_summary(matches, t, int(y))

print("Text summaries written to", TEXTDIR)
con.close()