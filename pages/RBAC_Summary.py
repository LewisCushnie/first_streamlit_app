import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
from connection import init_connection, run_query

conn = init_connection()

#============================= PAGE STARTS =================================

st.title('RBAC Roles Summary')

all_RBAC_roles = run_query("select CREATED_ON, NAME, COMMENT, OWNER from roles;")
st.header("Roles Summary:")
st.dataframe(all_RBAC_roles)

# Stop streamlit from running past this point
#st.stop()