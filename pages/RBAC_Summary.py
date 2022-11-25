import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

st.title('RBAC Roles Summary')

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

# Initialize snowflake connection object
conn = init_connection()

# Funtion to perform queries from the database.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

all_RBAC_roles = run_query("select * from roles;")
st.header("Roles Summary:")
st.dataframe(all_RBAC_roles)

# Stop streamlit from running past this point
st.stop()