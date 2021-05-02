import streamlit as st 

def setup():
    st.write("""
    Bienvenue sur ma première webapp!
    """)


    a = st.sidebar.radio('Choose dataset:', ['Ball', 'Player'])


    col1, col2 = st.beta_columns(2)
    col1.subheader('Ball')
    col2.subheader('Player')



if __name__ == '__main__':

    setup()