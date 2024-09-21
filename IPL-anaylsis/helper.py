import plotly.express as px
import streamlit as st

def Most_Played_Team(Matches):
    Most_Played_Team = (Matches['team1'].value_counts() + Matches['team2'].value_counts()).sort_values(ascending=False)
    Most_Played_Team_df = Most_Played_Team.reset_index()
    Most_Played_Team_df.columns = ['Team', 'Matches Played']
    return Most_Played_Team_df

def Season_Winner(Matches):
    Season = Matches['season'].dropna().unique().tolist()
    Season.sort()
    Season.insert(0, 'Overall')

    Winner = Matches['winner'].dropna().unique().tolist()
    Winner = [str(winner) for winner in Winner]  # Convert all elements to strings
    Winner.sort()
    Winner.insert(0, 'Overall')
    return Season, Winner

def fetch_Season_Winner(Matches,season, winner):
    seasonwinner = Matches.drop_duplicates('season', keep='last')[['season','winner']].sort_values('season').reset_index(drop=True)
    seasonwinner.columns = ['Season', 'Winner']
    temp_df = None

    if season == 'Overall' and winner == 'Overall':
        temp_df = seasonwinner
    elif season == 'Overall' and winner != 'Overall':
        temp_df = seasonwinner[seasonwinner['Winner'] == winner]
    elif season != 'Overall' and winner == 'Overall':
        temp_df = seasonwinner[seasonwinner['Season'] == season]
    elif season != 'Overall' and winner != 'Overall':
        temp_df = seasonwinner[(seasonwinner['Season'] == season) & (seasonwinner['Winner'] == winner)]

    if temp_df is not None:
        x = temp_df.sort_values(by='Season', ascending=True).reset_index(drop=True)
        return x

def Batsman_Run(Deliveries):
    Batsman = Deliveries['batsman'].dropna().unique().tolist()
    Batsman = [str(batsman) for batsman in Batsman]
    Batsman.sort()
    Batsman.insert(0, 'Overall')
    return Batsman


def fetch_Batsman_Run(Deliveries,batsman):
    Batsman = Deliveries['batsman'].dropna().unique().tolist()
    Batsman = [str(batsman) for batsman in Batsman]
    Batsman.sort()
    Batsman.insert(0, 'Overall')

    Runs = Deliveries.groupby("batsman")['batsman_runs'].sum()
    Top_Player_Runs = Runs.sort_values(ascending=False)
    Top_Player_Runs_df = Top_Player_Runs.reset_index()
    Top_Player_Runs_df.columns = ['Batsman Name', 'Runs']

    temp_df = None

    if batsman == 'Overall':
        temp_df = Top_Player_Runs_df.head(25)
    else:
        temp_df = Top_Player_Runs_df[Top_Player_Runs_df['Batsman Name'] == batsman]

    if temp_df is not None and not temp_df.empty:
        x = temp_df.sort_values(by='Runs', ascending=False).reset_index(drop=True)
        return x

def Bolwer_Run(Deliveries):
    Bowler = Deliveries['bowler'].dropna().unique().tolist()
    Bowler = [str(bowler) for bowler in Bowler]
    Bowler.sort()
    Bowler.insert(0, 'Overall')
    return Bowler

def fetch_Bowler_Run(Deliveries,bowler):
    Bowler = Deliveries['bowler'].dropna().unique().tolist()
    Bowler = [str(bowler) for bowler in Bowler]
    Bowler.sort()
    Bowler.insert(0, 'Overall')

    Runs = Deliveries.groupby("bowler")['total_runs'].sum()
    Top_Bowler_Runs = Runs.sort_values(ascending=False)
    Top_Bowler_Runs_df = Top_Bowler_Runs.reset_index()
    Top_Bowler_Runs_df.columns = ['Bowler Name', 'Runs']

    temp_df = None

    if bowler == 'Overall':
        temp_df = Top_Bowler_Runs_df.head(25)
    else:
        temp_df = Top_Bowler_Runs_df[Top_Bowler_Runs_df['Bowler Name'] == bowler]

    if temp_df is not None and not temp_df.empty:
        x = temp_df.sort_values(by='Runs', ascending=False).reset_index(drop=True)
        return x

def boundry(Deliveries):
    deliveries = Deliveries[Deliveries['batsman_runs'].isin([4, 6])]
    Runs = deliveries['batsman_runs'].unique().tolist()

    Batsmans = Deliveries['batsman'].dropna().unique().tolist()
    Batsmans = [str(batsman) for batsman in Batsmans]
    Batsmans.sort()
    Batsmans.insert(0, 'Overall')
    return Runs, Batsmans


def count_boundaries(Deliveries,runs, batsman):
    mask = Deliveries['batsman_runs'] == runs
    boundaries = Deliveries[mask]

    player_hit_boundaries = boundaries.groupby('batsman')['batsman_runs'].count().reset_index(name='Runs')
    player_hit_boundaries = player_hit_boundaries.sort_values(by='Runs', ascending=False)
    player_hit_boundaries.columns = ['batsman', 'Runs']

    temp_df = None

    if runs != 'Overall' and batsman == 'Overall':
        temp_df = player_hit_boundaries.head(25)
    elif runs != 'Overall' and batsman != 'Overall':
        temp_df = player_hit_boundaries[player_hit_boundaries['batsman'] == batsman]

    if temp_df is not None and not temp_df.empty:
        print(temp_df)
    else:
        print("No data found for the specified conditions.")
    return temp_df.reset_index(drop=True)

def batsman(Deliveries):
    Batsmans = Deliveries['batsman'].dropna().unique().tolist()
    Batsmans = [str(batsman) for batsman in Batsmans]
    Batsmans.sort()
    return Batsmans

def batsman_scored(Deliveries, batsman_name):
    # Filter data for the selected batsman
    batsman_data = Deliveries[Deliveries['batsman'] == batsman_name]

    # Grouping by bowling team and summing runs
    runs_by_team = (
        batsman_data.groupby('bowling_team')['batsman_runs']
        .sum()
        .reset_index(name='Runs')
        .sort_values(by='Runs', ascending=False)  # Sort by Runs in descending order
    )

    # Reset the index to maintain a clean DataFrame
    runs_by_team.reset_index(drop=True, inplace=True)

    if batsman_name != 'Overall':
        # Prepare the DataFrame for plotting
        if not runs_by_team.empty:
            # Creating the bar graph with Plotly
            fig = px.bar(
                runs_by_team,
                x='bowling_team',
                y='Runs',
                title=f'Runs Scored by {batsman_name} Against Different Bowling Teams',
                labels={'bowling_team': 'Bowling Team', 'Runs': 'Runs Scored'},
                color='Runs',
                text='Runs'
            )
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig.update_layout(xaxis_tickangle=-45)
            return fig  # Return the Plotly figure
        else:
            print(f"No data found for {batsman_name}.")
            return None
    else:
        print(f"No data found for {batsman_name}.")
        return None


def season(Matches):
    season = Matches['season'].dropna().unique().tolist()
    season.sort()
    season.insert(0, 'Overall')
    return season

def orange_cap_holder(Deliveries,Matches,season):
    Merge = Deliveries.merge(Matches, left_on="match_id", right_on='id')
    Orange_Cap = Merge.groupby(['season', 'batsman'])['batsman_runs'].sum().sort_values(ascending=False).reset_index()
    Orange_Cap_Holders = Orange_Cap.drop_duplicates(subset='season', keep='first').sort_values('season')[['season', 'batsman']]
    Orange_Cap_Holders.reset_index(drop=True)
    Orange_Cap_Holders.columns = ['Season', 'Batsman']
    temp_df = None

    if season == 'Overall':
        temp_df = Orange_Cap_Holders
    else:
        temp_df = Orange_Cap_Holders[Orange_Cap_Holders['Season'] == season]

    if temp_df is not None and not temp_df.empty:
        x = temp_df.sort_values(by='Season', ascending=True).reset_index(drop=True)
        return x