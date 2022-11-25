import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

st.title('Snowflake Connectivity Demo')

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select name, credits_used from metering_history")
my_data_rows = my_cur.fetchall()
st.header("Roles:")
st.dataframe(my_data_rows)

# Stop streamlit from running past this point
st.stop()

# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('from streamlit')")
    return "Thanks for adding" + new_fruit
    
add_my_fruit = st.text_input('What fruit would you like to add')
if st.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  st.text(back_from_function)

st.header("The fruit load list contains:")
# Snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
    
# Add button to load fruit
if st.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  st.dataframe(my_data_rows)
