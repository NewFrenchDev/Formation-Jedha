import streamlit as st 
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import os
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('.env')

def filedownload(dataframe):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV file</a>'
    return href
 
@st.cache
def load_data(year, team):
    records = None
    df=None
    try:
        # connection = psycopg2.connect(host=os.environ.get('HOST'), database=os.environ.get('NAME'), 
        #                             user=os.environ.get('USER'), password=os.environ.get('PASSWORD'),
        #                             port=os.environ.get('PORT'))
        cnx = create_engine(f"postgresql+psycopg2://{os.environ.get('USER')}:{os.environ.get('PASSWORD')}@{os.environ.get('HOST')}:{os.environ.get('PORT')}/{os.environ.get('NAME')}")
        # print('Connected')
        # cursor = connection.cursor()
        # # Print PostgreSQL details
        # print("PostgreSQL server information")
        # print(connection.get_dsn_parameters(), "\n")
        # # Executing a SQL query
        # cursor.execute("SELECT version();")
        # # Fetch result
        # record = cursor.fetchone()
        # print("You are connected to - ", record, "\n")
        # # Fetch result
        # cursor.execute("SELECT * FROM players_boxscore LIMIT 100")
        # record = cursor.fetchall()
        df = pd.read_sql_query(f"SELECT * FROM players_boxscore", con=cnx, parse_dates=['Game Date'])
        df = df[df['Game Date'].dt.year == year]
    except Exception as e:
        print('Unable to connect to the database', e)
    finally:
        return df

def setup():
    st.title("ML-Ball")

    st.write("""
    # Bienvenue sur ma première webapp!
    """)

    st.time_input('Time entry')

    connected = st.button('Connect to Database Postgresql')

    st.sidebar.header('User Input Features')
    a = st.sidebar.radio('Choose dataset:', ['Ball', 'Player'])
    selected_year = st.sidebar.selectbox('Year', list(reversed(range(2000, 2022))))
    selected_team = st.sidebar.selectbox('Team', ['WAS', 'TOR', 'LAL'])

    if connected:
        test = load_data(selected_year, selected_team)
        test

        st.markdown(filedownload(test), unsafe_allow_html=True)

    st.file_uploader('File uploader')

    

    col1, col2 = st.beta_columns(2)
    col1.subheader('Ball')
    col2.subheader('Player')


if __name__ == '__main__':

    setup()