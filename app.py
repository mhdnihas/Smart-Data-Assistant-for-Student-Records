from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import sqlite3

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to read SQL query and return rows
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Prompt for Gemini model
prompt = ["""
    You are the expert in converting English questions into SQL queries! 
    The SQL Database has a student table with the following columns: 
    NAME, AGE, GENDER, CLASS, SECTION, MARKS.
    For example:
    1. How many records are present? -> select * from student;
    2. Who is studying Mern Stack? -> select * from student where CLASS='Mern Stack';
    Please note that the SQL code should not include '```' at the beginning or end, and should not have the word 'sql'.
"""]

# Set the page configuration
st.set_page_config(page_title="SQL Query Generator with Gemini", page_icon=":robot_face:", layout="centered")

# Title and Header styling
st.markdown("<h1 style='text-align: center; color: #3366cc;'>Gemini SQL Query Generator</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ff6600;'>Ask questions, get SQL queries, and retrieve data!</h3>", unsafe_allow_html=True)

# Input section for the user's question
st.markdown("<h4 style='color: #006600;'>Enter your question about the student database:</h4>", unsafe_allow_html=True)
question = st.text_input("", placeholder="E.g., How many students are in Data Science?", key='input')

# Submit button with styling
submit = st.button("Generate SQL Query", help="Click to generate SQL and retrieve data")

# If the user submits a question
if submit:
    if question:
        sql_query = get_gemini_response(question=question, prompt=prompt)
        st.markdown("<h4 style='color: #003366;'>Generated SQL Query:</h4>", unsafe_allow_html=True)
        st.code(sql_query, language='sql')
        
        # Fetch and display data from the database
        response = read_sql_query(sql=sql_query, db="student.db")
        
        # Show the response in a visually appealing format
        if response:
            st.markdown("<h4 style='color: #cc0000;'>Query Results:</h4>", unsafe_allow_html=True)
            for row in response:
                st.write(row)
        else:
            st.error("No records found or invalid query!")
    else:
        st.warning("Please enter a question before submitting.")
