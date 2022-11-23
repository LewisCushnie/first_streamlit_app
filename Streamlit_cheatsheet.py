# STREAMLIT CHEAT SHEET WITH WORKING FEATURES AND CODE

# imports
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

# main titles
streamlit.title('This is how you add a title')
streamlit.header('This is how you create a header')
streamlit.text('This is how you add text')

# ----------------------------------------------------------------------------------
# WORKING WITH PANADAS DATAFRAMES 
# ----------------------------------------------------------------------------------
streamlit.header('Reading a CSV into a dataframe')

# reading a csv into a df
fruit_df = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
fruit_df = fruit_df.set_index('Fruit')

# Display the raw df on page.
streamlit.header('Raw dataframe')
streamlit.dataframe(fruit_df)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(fruit_df.index),['Avocado','Strawberries'])
fruits_to_show = fruit_df.loc[fruits_selected]

# Display the filtered df on the page.
streamlit.header('Dataframe filtered using the pick list')
streamlit.dataframe(fruits_to_show)

# ----------------------------------------------------------------------------------
# WORKING WITH APIS
# ----------------------------------------------------------------------------------
streamlit.header("Fruityvice Fruit Advice from API response")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to start")
  else:
    # streamlit.write('The user entered ', fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # Normalise json response
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # Output to screen as table
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()

## Allow the end user to add a fruit to the list
#add_my_fruit = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', add_my_fruit)
## my_cur.execute("insert into fruit_load_list values ('from streamlit')")

# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('from streamlit')")
    return "Thanks for adding" + new_fruit
    
add_my_fruit = streamlit.text_input('What fruit would you like to add')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("select * from fruit_load_list")
#my_data_rows = my_cur.fetchall()
#streamlit.header("The fruit load list contains:")
#streamlit.dataframe(my_data_rows)

streamlit.header("The fruit load list contains:")
# Snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
    
# Add button to load fruit
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)
  
# Stop streamlit from running past this point
streamlit.stop()

# Test test test
