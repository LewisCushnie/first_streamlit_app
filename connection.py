import streamlit as st
import snowflake.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    conn = snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

    conn.cursor().execute("ALTER SESSION SET QUERY_TAG = 'StreamlitQuery'")

    if 'conn' not in st.session_state:
        st.session_state['conn'] = conn

    return conn

# Funtion to perform queries from the database.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with st.session_state['conn'].cursor() as cur:
        cur.execute(query)
        return cur.fetchall()