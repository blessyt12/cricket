# cricket_stats_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Load data
df = pd.read_csv("ODI Cricket Data new1 (2).csv")

# Set visual style
sns.set(style="whitegrid")

# Title
st.title("🏏 ODI Cricket Player Stats Explorer")

# Function to show player stats
def show_player_stats(player_name):
    player_data = df[df['player_name'].str.lower() == player_name.lower()]

    if player_data.empty:
        st.error(f"No data found for '{player_name}'. Please check the spelling.")
        return

    player = player_data.iloc[0]

    st.subheader(f"Stats for {player['player_name']} ({player['role']} - {player['team']})")

    st.markdown(f"""
    **Total Matches:** {player['total_matches_played']}  
    **Total Runs:** {player['total_runs']}  
    **Strike Rate:** {player['strike_rate']}  
    **Batting Average:** {player['average']}  
    **Balls Faced:** {player['total_balls_faced']}  
    **Wickets Taken:** {player['total_wickets_taken']}  
    **Runs Conceded:** {player['total_runs_conceded']}  
    **Overs Bowled:** {player['total_overs_bowled']}  
    **Player of the Match Awards:** {player['player_of_match_awards']}  
    **Matches Won:** {player['matches_won']}  
    **Matches Lost:** {player['matches_lost']}  
    **Win Percentage:** {player['percentage']}%
    """)

    # Plotting
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    axs[0].bar(['Runs', 'Balls Faced'], [player['total_runs'], player['total_balls_faced']], color='skyblue')
    axs[0].set_title('Batting Performance')

    axs[1].bar(['Wickets', 'Runs Conceded'], [player['total_wickets_taken'], player['total_runs_conceded']], color='salmon')
    axs[1].set_title('Bowling Performance')

    axs[2].pie(
        [player['matches_won'], player['matches_lost']],
        labels=['Won', 'Lost'],
        autopct='%1.1f%%',
        colors=['green', 'red']
    )
    axs[2].set_title('Match Results')

    st.pyplot(fig)

    # Fun Quote
    quotes = [
        "'You don't win or lose the games because of the 11 you select. You win or lose with what those 11 do on the field.' - Rahul Dravid",
        "'No dream is ever chased alone.' - Sachin Tendulkar",
        "'First of all, convince yourself that you are the best because the rest of the world is going to go proving this to others.' - Wasim Akram",
        "'Compromise for your dream. But never compromise on your dream.' - MS Dhoni"
    ]
    st.success("💬 " + random.choice(quotes))

# Smart query handler
def handle_query(query):
    query = query.lower()
    if "most runs" in query:
        top = df.loc[df['total_runs'].idxmax()]
        st.info(f"🏏 Most Runs: **{top['player_name']}** - {top['total_runs']} runs")
        return True
    elif "most wickets" in query:
        top = df.loc[df['total_wickets_taken'].idxmax()]
        st.info(f"🎯 Most Wickets: **{top['player_name']}** - {top['total_wickets_taken']} wickets")
        return True
    elif "best average" in query:
        top = df.loc[df['average'].idxmax()]
        st.info(f"📈 Best Batting Average: **{top['player_name']}** - {top['average']}")
        return True
    elif "top bowlers" in query:
        top_bowlers = df.sort_values(by='total_wickets_taken', ascending=False).head(5)
        st.subheader("Top 5 Bowlers")
        for i, row in top_bowlers.iterrows():
            st.write(f"{row['player_name']} - {row['total_wickets_taken']} wickets")
        return True
    elif "strike rate" in query:
        top = df.loc[df['strike_rate'].idxmax()]
        st.info(f"⚡ Highest Strike Rate: **{top['player_name']}** - {top['strike_rate']}")
        return True
    elif "most matches" in query:
        top = df.loc[df['total_matches_played'].idxmax()]
        st.info(f"📅 Most Matches Played: **{top['player_name']}** - {top['total_matches_played']} matches")
        return True
    elif "all-rounder" in query or "allrounder" in query:
        allrounders = df[df['role'].str.lower().str.contains("allrounder")]
        top = allrounders.sort_values(by=['total_runs', 'total_wickets_taken'], ascending=False).head(5)
        st.subheader("Top All-Rounders")
        for _, row in top.iterrows():
            st.write(f"{row['player_name']} - Runs: {row['total_runs']}, Wickets: {row['total_wickets_taken']}")
        return True
    elif "player of the match" in query:
        top = df.loc[df['player_of_match_awards'].idxmax()]
        st.info(f"🏆 Most Player of the Match Awards: **{top['player_name']}** - {top['player_of_match_awards']} awards")
        return True
    return False

# Sidebar Interaction
st.sidebar.title("📊 Query Options")
query_input = st.sidebar.text_input("Ask a question (e.g., 'most runs'):")

if query_input:
    handled = handle_query(query_input)
    if not handled:
        st.sidebar.warning("Couldn't understand the query. Try again!")

# Role Selection
st.subheader("Select a Role")
role = st.selectbox("Choose role", ["Batsman", "Bowler", "All-Rounder"])

# Normalize role
role_map = {
    "Batsman": "batter",
    "Bowler": "bowler",
    "All-Rounder": "allrounder"
}
normalized_role = role_map[role]
filtered_players = df[df['role'].str.lower() == normalized_role]

# Leaderboard
if normalized_role == "batter":
    top3 = filtered_players.sort_values(by="total_runs", ascending=False).head(3)
    metric = "total_runs"
elif normalized_role == "bowler":
    top3 = filtered_players.sort_values(by="total_wickets_taken", ascending=False).head(3)
    metric = "total_wickets_taken"
else:
    df["combo_score"] = df["total_runs"] + df["total_wickets_taken"]
    top3 = filtered_players.sort_values(by="combo_score", ascending=False).head(3)
    metric = "combo_score"

st.subheader(f"Top 3 {role}s")
for _, row in top3.iterrows():
    st.write(f"- {row['player_name']} → {metric.replace('_', ' ').title()}: {row[metric]}")

# Player selection
player_name = st.selectbox("Choose a player to view detailed stats:", filtered_players['player_name'].unique())
show_player_stats(player_name)
