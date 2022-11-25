import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
from snowflake_demo import run_query

st.title('RBAC Roles Summary')

all_RBAC_roles = run_query("select * from roles;")
st.header("Roles Summary:")
st.dataframe(all_RBAC_roles)

# Stop streamlit from running past this point
st.stop()