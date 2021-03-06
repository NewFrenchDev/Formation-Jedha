import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

DATE_FORMAT = '%m/%d/%Y'
PLAYER_BOXSCORE_PATH = os.path.join('data', 'players', 'players-boxscores.csv') 

#Players Data
boxscore = pd.read_csv(PLAYER_BOXSCORE_PATH, sep=';', index_col=False)
unique_players = boxscore['Player'].unique()

def highlight(val):
    color = 'red' if val == 'L' else 'green'
    return f'background-color: {color}'

def dashboard_first_row():
    #Row1----------------------------------------------
    row1_1, row1_spacer, row1_2 = st.beta_columns([1, 2, 1])

    with row1_1:
        player_selected = st.selectbox('Player', options=unique_players)
        number_of_game = int(boxscore['Player'].value_counts()[player_selected])

    with row1_2:
        number_selected = st.slider('Number of Games', max_value=number_of_game, value=20)

    return player_selected, number_selected

def dashboard_second_row(player, number_of_game):
    #Row2-----------------------------------------------
    # row2_1, row2_spacer, row2_2 = st.beta_columns([2, 0.5, 2])

    # Game Log
    player_data = boxscore.loc[boxscore['Player'] == player].copy()

    player_data.drop(columns=['Unnamed: 0', 'Player', 'Player_Id', 'Team_Id', 'Game_Id'], inplace=True)
    player_data['Game Date'] = player_data['Game Date'].map(lambda x: datetime.strptime(x, DATE_FORMAT).date())
    player_data.sort_values(by='Game Date', ascending=False, inplace=True)
    player_data.reset_index(drop=True, inplace=True)
    player_data[['W/L']].style.applymap(highlight)
    st.dataframe(player_data.iloc[:number_of_game])