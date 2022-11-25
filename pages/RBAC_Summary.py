import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

st.title('RBAC Roles Summary')

all_RBAC_roles = run_query("select * from roles;")
st.header("Roles Summary:")
st.dataframe(all_RBAC_roles)