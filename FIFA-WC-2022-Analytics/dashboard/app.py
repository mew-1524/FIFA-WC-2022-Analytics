import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


# PAGE CONFIG


st.set_page_config(
    page_title="FIFA World Cup 2022 Analytics",
    layout="wide"
)

st.title("⚽ FIFA World Cup 2022 Complete Analytics Dashboard")


# LOAD DATA


current_dir = os.path.dirname(__file__)

file_path = os.path.join(
    current_dir,
    "../data/Fifa_world_cup_matches.csv"
)

matches = pd.read_csv(file_path)

# DATASET PREVIEW


st.header("📄 Dataset Preview")

st.write(matches.head())

matches = pd.read_csv(file_path)

# Convert possession to float

matches['possession team1'] = (
    matches['possession team1']
    .astype(str)
    .str.replace('%', '')
    .astype(float)
)

matches['possession team2'] = (
    matches['possession team2']
    .astype(str)
    .str.replace('%', '')
    .astype(float)
)

# -------------------------------------------------
# DATASET INFORMATION
# -------------------------------------------------

st.header("📊 Dataset Information")

st.write("Total Matches:", matches.shape[0])

st.write("Total Columns:", matches.shape[1])

# -------------------------------------------------
# TOTAL GOALS
# -------------------------------------------------

matches['total_goals'] = (
    matches['number of goals team1'] +
    matches['number of goals team2']
)

st.header("⚽ Goal Statistics")

total_goals = matches['total_goals'].sum()

avg_goals = total_goals / matches.shape[0]

st.write("Total Goals in Tournament:", total_goals)

st.write("Average Goals Per Match:", round(avg_goals, 2))


# HIGHEST SCORING MATCH


st.header("🔥 Highest Scoring Match")

highest_match = matches.sort_values(
    by='total_goals',
    ascending=False
)

st.write(highest_match[[
    'team1',
    'team2',
    'number of goals team1',
    'number of goals team2',
    'total_goals'
]].head(1))


# TOP SCORING TEAMS


st.header("🏆 Top Scoring Teams")

team1_goals = matches.groupby(
    'team1'
)['number of goals team1'].sum()

team2_goals = matches.groupby(
    'team2'
)['number of goals team2'].sum()

total_team_goals = team1_goals.add(
    team2_goals,
    fill_value=0
)

top_teams = total_team_goals.sort_values(
    ascending=False
)

st.write(top_teams)

# -------------------------------------------------
# TOP SCORING TEAMS GRAPH
# -------------------------------------------------

fig1, ax1 = plt.subplots(figsize=(12, 6))

top_teams.head(10).plot(
    kind='bar',
    ax=ax1
)

plt.title("Top Scoring Teams")

plt.xlabel("Teams")

plt.ylabel("Goals")

st.pyplot(fig1)

# -------------------------------------------------
# POSSESSION ANALYSIS
# -------------------------------------------------

st.header("📈 Average Possession Analysis")

team1_possession = matches.groupby(
    'team1'
)['possession team1'].mean()

team2_possession = matches.groupby(
    'team2'
)['possession team2'].mean()

avg_possession = team1_possession.add(
    team2_possession,
    fill_value=0
) / 2

avg_possession = avg_possession.sort_values(
    ascending=False
)

st.write(avg_possession)

# -------------------------------------------------
# POSSESSION GRAPH
# -------------------------------------------------

fig2, ax2 = plt.subplots(figsize=(12, 6))

avg_possession.head(10).plot(
    kind='bar',
    ax=ax2
)

plt.title("Top Possession Teams")

plt.xlabel("Teams")

plt.ylabel("Possession %")

st.pyplot(fig2)

# TOTAL ATTEMPTS ANALYSIS


st.header("🎯 Shot Attempts Analysis")

team1_attempts = matches.groupby(
    'team1'
)['total attempts team1'].sum()

team2_attempts = matches.groupby(
    'team2'
)['total attempts team2'].sum()

total_attempts = team1_attempts.add(
    team2_attempts,
    fill_value=0
)

top_attempts = total_attempts.sort_values(
    ascending=False
)

st.write(top_attempts)


# ATTEMPTS GRAPH

fig3, ax3 = plt.subplots(figsize=(12, 6))

top_attempts.head(10).plot(
    kind='bar',
    ax=ax3
)

plt.title("Teams with Most Attempts")

plt.xlabel("Teams")

plt.ylabel("Attempts")

st.pyplot(fig3)


# PASSING ANALYSIS


st.header("🎯 Passing Analysis")

team1_passes = matches.groupby(
    'team1'
)['passes completed team1'].sum()

team2_passes = matches.groupby(
    'team2'
)['passes completed team2'].sum()

total_passes = team1_passes.add(
    team2_passes,
    fill_value=0
)

top_passing = total_passes.sort_values(
    ascending=False
)

st.write(top_passing)


# PASSING GRAPH


fig4, ax4 = plt.subplots(figsize=(12, 6))

top_passing.head(10).plot(
    kind='bar',
    ax=ax4
)

plt.title("Best Passing Teams")

plt.xlabel("Teams")

plt.ylabel("Completed Passes")

st.pyplot(fig4)

# DISCIPLINE ANALYSIS


st.header("🟨 Discipline Analysis")

team1_yellow = matches.groupby(
    'team1'
)['yellow cards team1'].sum()

team2_yellow = matches.groupby(
    'team2'
)['yellow cards team2'].sum()

yellow_cards = team1_yellow.add(
    team2_yellow,
    fill_value=0
)

yellow_cards = yellow_cards.sort_values(
    ascending=False
)

st.write(yellow_cards)


# YELLOW CARD GRAPH


fig5, ax5 = plt.subplots(figsize=(12, 6))

yellow_cards.head(10).plot(
    kind='bar',
    ax=ax5
)

plt.title("Teams with Most Yellow Cards")

plt.xlabel("Teams")

plt.ylabel("Yellow Cards")

st.pyplot(fig5)


# OFFSIDE ANALYSIS


st.header("🚩 Offside Analysis")

team1_offside = matches.groupby(
    'team1'
)['offsides team1'].sum()

team2_offside = matches.groupby(
    'team2'
)['offsides team2'].sum()

offsides = team1_offside.add(
    team2_offside,
    fill_value=0
)

offsides = offsides.sort_values(
    ascending=False
)

st.write(offsides)

# -------------------------------------------------
# TEAM SELECTOR
# -------------------------------------------------

st.header("🔍 Team Specific Analysis")

teams = sorted(matches['team1'].unique())

selected_team = st.selectbox(
    "Select Team",
    teams
)

team_matches = matches[
    (matches['team1'] == selected_team) |
    (matches['team2'] == selected_team)
]

st.write(team_matches)

# -------------------------------------------------
# TEAM STATISTICS
# -------------------------------------------------

home_matches = matches[
    matches['team1'] == selected_team
]

away_matches = matches[
    matches['team2'] == selected_team
]

goals_scored = (
    home_matches['number of goals team1'].sum() +
    away_matches['number of goals team2'].sum()
)

goals_conceded = (
    home_matches['number of goals team2'].sum() +
    away_matches['number of goals team1'].sum()
)

attempts = (
    home_matches['total attempts team1'].sum() +
    away_matches['total attempts team2'].sum()
)

passes = (
    home_matches['passes completed team1'].sum() +
    away_matches['passes completed team2'].sum()
)

yellow = (
    home_matches['yellow cards team1'].sum() +
    away_matches['yellow cards team2'].sum()
)

red = (
    home_matches['red cards team1'].sum() +
    away_matches['red cards team2'].sum()
)

st.subheader(f"{selected_team} Statistics")

st.write("Matches Played:", team_matches.shape[0])

st.write("Goals Scored:", goals_scored)

st.write("Goals Conceded:", goals_conceded)

st.write("Total Attempts:", attempts)

st.write("Completed Passes:", passes)

st.write("Yellow Cards:", yellow)

st.write("Red Cards:", red)
# -------------------------------------------------
# TEAM JOURNEY ANALYSIS
# -------------------------------------------------

st.header("🌍 Team Journey Analysis")

# Create team list
all_teams = sorted(
    list(
        set(matches['team1']).union(
            set(matches['team2'])
        )
    )
)

# Team selector
selected_team = st.selectbox(
    "Select Team for Full Analysis",
    all_teams
)

# Filter matches
team_matches = matches[
    matches['team1'].str.lower().str.contains(
        selected_team.lower()
    ) |
    matches['team2'].str.lower().str.contains(
        selected_team.lower()
    )
]

# Show matches
st.subheader(f"{selected_team} Match Journey")

st.write(team_matches[[
    'team1',
    'team2',
    'number of goals team1',
    'number of goals team2',
    'date',
    'category'
]])

# -------------------------------------------------
# TEAM STATISTICS
# -------------------------------------------------

home_matches = matches[
    matches['team1'].str.lower() ==
    selected_team.lower()
]

away_matches = matches[
    matches['team2'].str.lower() ==
    selected_team.lower()
]

# Goals scored
goals_scored = (
    home_matches['number of goals team1'].sum() +
    away_matches['number of goals team2'].sum()
)

# Goals conceded
goals_conceded = (
    home_matches['number of goals team2'].sum() +
    away_matches['number of goals team1'].sum()
)

# Possession
avg_possession = (
    home_matches['possession team1'].mean() +
    away_matches['possession team2'].mean()
) / 2

# Attempts
total_attempts = (
    home_matches['total attempts team1'].sum() +
    away_matches['total attempts team2'].sum()
)

# Passes
total_passes = (
    home_matches['passes completed team1'].sum() +
    away_matches['passes completed team2'].sum()
)

# Yellow cards
yellow_cards = (
    home_matches['yellow cards team1'].sum() +
    away_matches['yellow cards team2'].sum()
)

# Red cards
red_cards = (
    home_matches['red cards team1'].sum() +
    away_matches['red cards team2'].sum()
)

# -------------------------------------------------
# DISPLAY STATS
# -------------------------------------------------

st.subheader(f"{selected_team} Tournament Statistics")

st.write("Matches Played:", team_matches.shape[0])

st.write("Goals Scored:", goals_scored)

st.write("Goals Conceded:", goals_conceded)

st.write(
    "Average Possession:",
    round(avg_possession, 2)
)

st.write("Total Attempts:", total_attempts)

st.write("Completed Passes:", total_passes)

st.write("Yellow Cards:", yellow_cards)

st.write("Red Cards:", red_cards)

st.success("FIFA World Cup 2022 Complete Analytics Dashboard Ready ✅")