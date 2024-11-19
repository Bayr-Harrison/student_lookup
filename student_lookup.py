import os
import pg8000
import pandas as pd
import streamlit as st

# Set a simple password
#PASSWORD = os.environ["APP_PASSWORD"]

# Password input for access
#password = st.text_input("Enter Password", type="password")
#if password != PASSWORD:
    #st.warning("Incorrect password")
    #st.stop()
#else:
    #st.success("Access granted!")

# Function to establish a database connection
def get_database_connection():
    db_connection = pg8000.connect(
        database=os.environ["SUPABASE_DB_NAME"],
        user=os.environ["SUPABASE_USER"],
        password=os.environ["SUPABASE_PASSWORD"],
        host=os.environ["SUPABASE_HOST"],
        port=os.environ["SUPABASE_PORT"]
    )
    return db_connection

# Function to fetch student data by IATC ID
def fetch_student_data(iatc_id):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()

    # SQL query to fetch the student data
    query = """
    SELECT 
        iatc_id,
        password,
        name,
        nat_id,
        class
    FROM 
        student_list
    WHERE 
        iatc_id = %s
    """

    # Execute the query
    db_cursor.execute(query, (iatc_id,))
    rows = db_cursor.fetchall()
    column_names = ['IATC ID', 'Password', 'Name', 'National ID', 'Class']

    # Close the cursor and connection
    db_cursor.close()
    db_connection.close()

    # Convert the results to a DataFrame
    data = pd.DataFrame(rows, columns=column_names)
    return data

# Streamlit interface
st.title("Search Student by IATC ID")

# Input field for IATC ID
iatc_id = st.text_input("Enter the IATC ID:")

# Button to fetch data
if st.button("Search"):
    if iatc_id:
        student_data = fetch_student_data(iatc_id)

        # Display the result
        if not student_data.empty:
            st.write("Student Details:")
            st.dataframe(student_data)
        else:
            st.warning("No student found with the entered IATC ID.")
    else:
        st.warning("Please enter a valid IATC ID.")
