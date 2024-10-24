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
    You are an expert at converting English questions into SQL queries! 
    The SQL Database has a student table with the following columns: 
    NAME, AGE, GENDER, CLASS, SECTION, MARKS.
    Examples:
    1. How many records are present? -> select * from student;
    2. Who is studying Mern Stack? -> select * from student where CLASS='Mern Stack';

    also the sql code should not have ``` in beginning or end and sql word in output

"""]

# Set the page configuration
st.set_page_config(page_title="Ask Anything: Instantly Retrieve Insights from Student Records", page_icon="🤖", layout="centered")

# Custom CSS for colors and styling
st.markdown("""
    <style>
        .main-container {
            background-color: #f4f4f9;
            padding: 20px;
            border-radius: 8px;
        }
        .title-text {
            text-align: center;
            color: #2E86C1;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .sub-header {
            text-align: center;
            color: #F39C12;
            margin-bottom: 30px;
        }
        .input-label {
            color: #117864;
            font-size: 16px;
            font-weight: bold;
        }
        .stButton>button {
            background-color: #2E86C1;
            color: white;
            border-radius: 5px;
            padding: 8px 15px;
            font-size: 16px;
            margin-top: 15px;
        }
        .stButton>button:hover {
            background-color: #21618C;
        }
        .result-label {
            color: #1C2833;
            font-size: 18px;
            margin-top: 20px;
        }
        .no-records {
            color: #E74C3C;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        }
        .sidebar-container {
            background-color: #EBF5FB;
            padding: 10px;
            border-radius: 10px;
        }
        .stAlert {
            background-color: #FADBD8;
            color: #E74C3C;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar with example questions
st.sidebar.markdown("<h3 style='color: #2E86C1;'>Example Questions</h3>", unsafe_allow_html=True)
st.sidebar.write("- give the information of all students ?")
st.sidebar.write("- How many students are in Data Science?")
st.sidebar.write("- Show students in Mern Stack class.")
st.sidebar.write("- What is the average marks of students?")
st.sidebar.write("- List all students above 21 years of age.")

# Main container for chatbot UI
with st.container():
    st.markdown("<h1 class='title-text'>Effortlessly Turn Your Questions Into Actionable Data</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='sub-header'>Ask your questions, and get the data you need!</h4>", unsafe_allow_html=True)

    # Input section for the user's question
    st.markdown("<h4 class='input-label'>Enter your question about the student database:</h4>", unsafe_allow_html=True)
    question = st.text_input("", placeholder="E.g., How many students are in Data Science?", key='input')

    # Submit button
    submit = st.button("Show Results")

    # Handle query generation and display results
    if submit:
        if question:
            sql_query = get_gemini_response(question=question, prompt=prompt)
            
            # Fetch and display data from the database
            response = read_sql_query(sql=sql_query, db="student.db")
            
            if response:
                st.markdown("<h4 class='result-label'>Your Data Insights:</h4>", unsafe_allow_html=True)
                for row in response:
                    st.write(row)
            else:
                st.error("No records found or invalid query!")
        else:
            st.warning("Please enter a question before submitting.")
