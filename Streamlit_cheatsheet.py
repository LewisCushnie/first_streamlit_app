# STREAMLIT CHEAT SHEET WITH WORKING FEATURES AND CODE

# imports
import streamlit
import pandas
import requests
import snowflake.connector

# This library returns the error that is presented by a website/api when you put a wrong input
# e.g https://websitename/page/dhjfdjhdfhjfd would return '404 page not found'
from urllib.error import URLError

# main titles
streamlit.title('This is how you add a title')
streamlit.header('This is how you create a header')
streamlit.text('This is how you add text')
streamlit.text('--------------------------------------------------------------------')

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

# Filtering using a PICK LIST
streamlit.header('Dataframe filtered using the pick list')
# Multiselect list
fruits_selected = streamlit.multiselect("Pick some fruits:", list(fruit_df.index),['Avocado','Strawberries'])
# filter using panda's .loc
fruits_to_show = fruit_df.loc[fruits_selected]

# Display the filtered df on the page.
streamlit.dataframe(fruits_to_show)

# ----------------------------------------------------------------------------------
# WORKING WITH APIS (AND JSON RESPONSE)
# ----------------------------------------------------------------------------------
streamlit.header("Displaying information from an API response")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')

  # if they haven't typed a fruit
  if not fruit_choice:
    streamlit.error("Please type a fruit to start")

  # if they have typed a fruit  
  else:
    streamlit.write('You entered ', fruit_choice)
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
    # Normalise json response
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # Output to screen as table
    streamlit.dataframe(fruityvice_normalized)

# If the user types in a wrong input, this will return the error directly from the API
except URLError as e:
  streamlit.error()

# NOTE, when working with booleans, no need to write if value == True, can instead write if value:
# likewise, rather than if value != true, can write if not value
# this also works for string/empty strings, lists/empty lists, etc.

streamlit.stop()

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
