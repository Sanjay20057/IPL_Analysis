import streamlit as st
import pandas as pd
import helper
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

Deliveries = pd.read_csv('C:/Users/sanja/Downloads/deliveries(1).csv')
Matches = pd.read_csv('C:/Users/sanja/Downloads/matches(1).csv')

st.sidebar.title('IPL Anaylsis')
st.sidebar.image(
    'https://files.ekmcdn.com/aswanicricket/images/2024-tata-ipl-ranges-510-c.gif?w=400&h=400&v=306D7880-3039-4F01-997D-E3EEA8E7C83F',
    width=200)
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Most Played Team','Season Winner','Batsman','Bowler','Boundries Anaylsis','Batsman Score','Orange Cap Holder')
)
if user_menu == 'Most Played Team':
    st.title('Most Played Team')

    Most_Played_Team = helper.Most_Played_Team(Matches)

    st.table(Most_Played_Team)
    st.title('Most Played Team')

    plt.figure(figsize=(12, 6))
    plt.plot(Most_Played_Team['Team'], Most_Played_Team['Matches Played'], marker='o', color='skyblue')
    plt.title('Most Played Teams')
    plt.xlabel('Teams')
    plt.ylabel('Matches Played')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    st.pyplot(plt)

    st.title('Most Played Team')

    fig = px.line(Most_Played_Team, x='Team', y='Matches Played', title='Most Played Teams', markers=True)
    fig.update_layout(xaxis_title='Teams', yaxis_title='Matches Played', xaxis_tickangle=-45)
    st.plotly_chart(fig)

if user_menu == 'Season Winner':
    st.sidebar.title('Season Winner')
    season, winner = helper.Season_Winner(Matches)

    Selected_season = st.sidebar.selectbox('Select Season', season)
    Selected_winner = st.sidebar.selectbox('Select Winner', winner)

    Season_Winner = helper.fetch_Season_Winner(Matches,Selected_season,Selected_winner)
    if Selected_season == 'Overall' and Selected_winner == 'Overall':
        st.title('Overall Season Winner')
    if Selected_season != 'Overall' and Selected_winner == 'Overall':
        st.header('Season Winner in ' + str(Selected_season))
    if Selected_season == 'Overall' and Selected_winner != 'Overall':
        st.title(Selected_winner + ' is Season Winner')
    if Selected_season != 'Overall' and Selected_winner != 'Overall':
        st.header(Selected_winner + ' is Season Winner in ' + str(Selected_season))
    st.table(Season_Winner)

    st.title('Season Winner')
    season = Matches.drop_duplicates('season', keep='last')[['season', 'winner']].sort_values('season').reset_index(
        drop=True)

    fig = px.bar(season, x='season', y='winner', title='Season Winners', text='winner', labels={'winner': 'Winner'})
    fig.update_layout(xaxis_title='Season', yaxis_title='Winner', xaxis_tickangle=-45)

    st.plotly_chart(fig)

    win_counts = season['winner'].value_counts().reset_index()
    win_counts.columns = ['Winner', 'Number of Wins']

    fig = px.bar(win_counts, x='Winner', y='Number of Wins', title='Number of Wins by Team', text='Number of Wins')
    fig.update_layout(xaxis_title='Teams', yaxis_title='Number of Wins', xaxis_tickangle=-45)

    st.plotly_chart(fig)

if user_menu == 'Batsman':
    st.sidebar.title('Batsman')
    batsman = helper.Batsman_Run(Deliveries)

    Selected_batsman = st.sidebar.selectbox('Select Batsman', batsman)

    Batsman = helper.fetch_Batsman_Run(Deliveries, Selected_batsman)
    if Selected_batsman == 'Overall':
        st.title('Top 25 Batsman Runs in Season 2008-2019')
    if Selected_batsman != 'Overall':
        st.header(Selected_batsman + ' Runs in Season 2008-2019')
    st.table(Batsman)

    Runs = Deliveries.groupby("batsman")['batsman_runs'].sum().sort_values(ascending=False)

    Top_Player_Runs = Runs.head(25).reset_index()
    Top_Player_Runs.columns = ['Batsman', 'Total Runs']

    fig = px.bar(Top_Player_Runs, x='Batsman', y='Total Runs', title='Top 25 Batsmen by Total Runs', text='Total Runs')
    fig.update_layout(xaxis_title='Batsman', yaxis_title='Total Runs', xaxis_tickangle=-45)
    st.plotly_chart(fig)

    Top_Player_Runs = Runs.head(25).reset_index()
    Top_Player_Runs.columns = ['Batsman', 'Total Runs']

    fig = px.bar(Top_Player_Runs, y='Batsman', x='Total Runs', title='Top 25 Batsmen by Total Runs', text='Total Runs',
                 orientation='h')
    fig.update_layout(yaxis_title='Batsman', xaxis_title='Total Runs')
    st.plotly_chart(fig)

if user_menu == 'Bowler':
    st.sidebar.title('Bowler')
    bowler = helper.Bolwer_Run(Deliveries)

    Selected_bowler = st.sidebar.selectbox('Select Bowler', bowler)

    Bowler = helper.fetch_Bowler_Run(Deliveries, Selected_bowler)
    if Selected_bowler == 'Overall':
        st.title('Top 25 Bowler Total Runs in Season 2008-2019')
    if Selected_bowler != 'Overall':
        st.header(Selected_bowler + ' Total Runs in Season 2008-2019')
    st.table(Bowler)

    st.title('Top 25 Bowlers by Total Runs')
    Ball = Deliveries.groupby("bowler")['total_runs'].sum().sort_values(ascending=False)
    Bowler_Runs = Ball.head(25).reset_index()
    Bowler_Runs.columns = ['Bowler', 'Total Runs']

    fig = px.line(Bowler_Runs, x='Bowler', y='Total Runs', title='Top 25 Bowlers by Total Runs', markers=True)
    fig.update_layout(xaxis_title='Bowler', yaxis_title='Total Runs', xaxis_tickangle=-45)
    st.plotly_chart(fig)

    Ball = Deliveries.groupby("bowler")['total_runs'].sum().sort_values(ascending=False)

    Bowler_Runs = Ball.head(25).reset_index()
    Bowler_Runs.columns = ['Bowler', 'Total Runs']

    fig = px.pie(Bowler_Runs, values='Total Runs', names='Bowler', title='Top 25 Bowlers by Total Runs')
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig)

if user_menu == 'Boundries Anaylsis':
    st.sidebar.title('Boundries Score')
    Runs, Batsmans = helper.boundry(Deliveries)

    Selected_Runs = st.sidebar.selectbox('Select Run', Runs)
    Selected_Batsmans = st.sidebar.selectbox('Select Batsman', Batsmans)

    Boundries = helper.count_boundaries(Deliveries,Selected_Runs, Selected_Batsmans)
    if Selected_Runs != 'Overall' and Selected_Batsmans == 'Overall':
        st.title('Top 25 Batsman Hit ' + str(Selected_Runs) + ' in Season 2008-2019')
    if Selected_Runs != 'Overall' and Selected_Batsmans != 'Overall':
        st.header(Selected_Batsmans + ' Hit ' + str(Selected_Runs) + ' in Season 2008-2019')
    st.table(Boundries)

    st.title('Histogram of Fours Hit by Batsmen')
    Mask1 = Deliveries['batsman_runs'] == 4
    Boundry_Four = Deliveries[Mask1]

    Player_Hit_Four = Boundry_Four.groupby('batsman')['batsman_runs'].count().reset_index()
    Player_Hit_Four.columns = ['Batsman', 'Fours Hit']

    fig = px.histogram(Player_Hit_Four, x='Fours Hit', nbins=20, title='Histogram of Fours Hit by Batsmen')
    fig.update_layout(xaxis_title='Number of Fours', yaxis_title='Count of Batsmen')
    st.plotly_chart(fig)

    st.title('Top 25 Batsmen by Sixes Hit')

    Mask2 = Deliveries['batsman_runs'] == 6
    Boundry_Six = Deliveries[Mask2]

    Player_Hit_Six = Boundry_Six.groupby('batsman')['batsman_runs'].count().sort_values(ascending=False).reset_index()
    Player_Hit_Six.columns = ['Batsman', 'Sixes Hit']

    fig3 = px.area(Player_Hit_Six.head(25), x='Batsman', y='Sixes Hit', title='Area Chart of Sixes Hit by Batsmen',
                   markers=True)
    fig3.update_layout(xaxis_title='Batsman', yaxis_title='Number of Sixes', xaxis_tickangle=-45)
    st.plotly_chart(fig3)

    Boundry_Four = Deliveries[Mask1]
    Player_Hit_Four = Boundry_Four.groupby('batsman')['batsman_runs'].count().reset_index()
    Player_Hit_Four.columns = ['Batsman', 'Fours']
    Player_Hit_Four = Player_Hit_Four.sort_values(by='Fours', ascending=False).head(25)

    Mask2 = Deliveries['batsman_runs'] == 6
    Boundry_Six = Deliveries[Mask2]
    Player_Hit_Six = Boundry_Six.groupby('batsman')['batsman_runs'].count().reset_index()
    Player_Hit_Six.columns = ['Batsman', 'Sixes']
    Player_Hit_Six = Player_Hit_Six.sort_values(by='Sixes', ascending=False).head(25)

    Player_Stats = Player_Hit_Four.merge(Player_Hit_Six, on='Batsman', how='outer').fillna(0)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=Player_Stats['Batsman'],
        y=Player_Stats['Fours'],
        mode='lines+markers',
        name='Fours',
        line=dict(color='blue'),
        marker=dict(symbol='circle')
    ))

    fig.add_trace(go.Scatter(
        x=Player_Stats['Batsman'],
        y=Player_Stats['Sixes'],
        mode='lines+markers',
        name='Sixes',
        line=dict(color='orange'),
        marker=dict(symbol='circle')
    ))

    fig.update_layout(
        title='Top Batsmen: Number of Fours and Sixes',
        xaxis_title='Batsman',
        yaxis_title='Count',
        xaxis_tickangle=-45,
        legend_title='Boundary Type'
    )

    st.title('Top Batsmen Performance')
    st.plotly_chart(fig)

if user_menu == 'Batsman Score':
    st.sidebar.title('Batsman Name')
    Batsman = helper.batsman(Deliveries)

    Selected_Batsman_Name = st.sidebar.selectbox('Select Batsman Name', Batsman)

    # Display batsman score table
    batsman_data = Deliveries[Deliveries['batsman'] == Selected_Batsman_Name]
    runs_by_team = (
        batsman_data.groupby('bowling_team')['batsman_runs']
        .sum()
        .reset_index(name='Runs')
        .sort_values(by='Runs', ascending=False)
    )

    if Selected_Batsman_Name != 'Overall':
        st.header(f"{Selected_Batsman_Name}'s Runs to Bowling Teams (2008-2019)")
    st.table(runs_by_team)

    # Get the Plotly figure and display it
    Batsman_plot = helper.batsman_scored(Deliveries, Selected_Batsman_Name)
    if Batsman_plot is not None:
        st.plotly_chart(Batsman_plot)  # Only plot if the figure is not None
    else:
        st.write(f"No data found for {Selected_Batsman_Name}.")

if user_menu == 'Orange Cap Holder':
    st.sidebar.title('Orange Cap Holder')
    Season = helper.season(Matches)

    Selected_season = st.sidebar.selectbox('Select Season', Season)

    Orange_Cap_Holder = helper.orange_cap_holder(Deliveries, Matches, Selected_season)
    if Selected_season == 'Overall':
        st.title('Overall Orange Cap Holder Batsman in Each Season')
    if Selected_season != 'Overall':
        st.header('Season ' + str(Selected_season) + ' Orange Cap Holder Batsman')
    st.table(Orange_Cap_Holder)

    Merge = Deliveries.merge(Matches, left_on="match_id", right_on='id')
    Orange_Cap = Merge.groupby(['season', 'batsman'])['batsman_runs'].sum().sort_values(ascending=False).reset_index()
    Orange_Cap_Holders = Orange_Cap.drop_duplicates(subset='season', keep='first').sort_values('season')[
        ['season', 'batsman']]
    Orange_Cap_Holders = Orange_Cap_Holders.reset_index(drop=True)

    # Encode batsman names for y-axis
    Orange_Cap_Holders['batsman_encoded'] = Orange_Cap_Holders['batsman'].factorize()[0]

    # Create the scatter plot
    fig = px.scatter(
        Orange_Cap_Holders,
        x='season',
        y='batsman_encoded',
        text='batsman',  # Show batsman names on the markers
        title='Scatter Plot of Orange Cap Holders',
        labels={'batsman_encoded': 'Batsman (encoded)', 'season': 'Season'}
    )

    # Update layout for better readability
    fig.update_traces(textposition='top center')
    fig.update_layout(
        xaxis_title='Season',
        yaxis_title='Batsman (encoded)',
        yaxis=dict(tickvals=list(range(len(Orange_Cap_Holders['batsman'].unique()))),
                   ticktext=Orange_Cap_Holders['batsman'].unique()),
        xaxis_tickangle=-45
    )

    # Streamlit title and plot display
    st.title("Orange Cap Holders Over Seasons")
    st.plotly_chart(fig)
