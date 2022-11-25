import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
from snowflake_demo import a

st.title('RBAC Roles Summary')
st.dataframe(a)

# Stop streamlit from running past this point
#st.stop()