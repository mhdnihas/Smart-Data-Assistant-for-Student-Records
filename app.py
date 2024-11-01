from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import sqlite3
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

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
    column_names = [description[0] for description in cur.description]
    conn.commit()
    conn.close()
    return rows, column_names

# Function to show database schema
def show_database_schema():
    st.image("schema.png", caption="Database Schema Diagram", use_column_width=True)

    schema_info = """
    ### Database Schema

    - **Student Table**:
        - **StudentID**: Unique identifier for each student.
        - **Name**: Name of the student.
        - **Age**: Age of the student.
        - **Gender**: Gender of the student.
        - **Class**: Class of the student.
        - **Section**: Section of the student.
        - **Place**: Place of residence of the student.
        - **DateOfBirth**: Date of birth of the student.
        - **CGPA**: Cumulative Grade Point Average.

    - **Course Table**:
        - **CourseID**: Unique identifier for each course.
        - **CourseName**: Name of the course.
        - **Credits**: Number of credits for the course.
        - **Semester**: Semester in which the course is offered.

    - **Enrollment Table**:
        - **EnrollmentID**: Unique identifier for each enrollment.
        - **StudentID**: Identifier for the student (foreign key).
        - **CourseID**: Identifier for the course (foreign key).
        - **EnrollmentDate**: Date when the student enrolled in the course.
        - **FinalGrade**: Final grade obtained by the student in the course.
        - **Status**: Enrollment status (e.g., active, completed).
    """
    st.markdown(schema_info)
    
    # Display schema image

# Prompt for Gemini model
prompt = ["""
    You are an SQL expert converting English questions into SQL queries. The database contains three tables:

    Student table with columns: StudentID, Name, Age, Gender, Class, Section, Place, DateOfBirth, and CGPA.
    Course table with columns: CourseID, CourseName, Credits, and Semester.
    Enrollment table with columns: EnrollmentID, StudentID, CourseID, EnrollmentDate, FinalGrade, and Status.
    
    Given a question, Write SQL queries to retrieve information from the SQLite database. 
    To support the database structure, use partial matching with the LIKE clause when searching course names, rather than exact matches. 
    Ensure the queries are correctly formatted, contain no comments, and do not include any code block markers.
"""]

st.set_page_config(page_title="Student Database Insights", page_icon="🤖", layout="centered")

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

# Sidebar for navigation
st.sidebar.markdown("<h3 style='color: #2E86C1;'>Navigation</h3>", unsafe_allow_html=True)
selected_option = st.sidebar.radio("Select Interface:", ("View Database Schema", "Ask a Question"))

# Interface for viewing database schema
if selected_option == "View Database Schema":
    show_database_schema()

# Interface for asking questions
elif selected_option == "Ask a Question":
    st.markdown("<h1 class='title-text'>Ask Your Questions About Student Records</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='sub-header'>Enter your question and get insights!</h4>", unsafe_allow_html=True)
    st.markdown("<h4 class='input-label'>Enter your question about the student database:</h4>", unsafe_allow_html=True)

    question = st.text_input(
        label="Question", 
        placeholder="E.g., How many students are in Data Science?",
        key='input',
        label_visibility="hidden"  
    )
    
    submit = st.button("Show Results")

    if submit:
        if question:
            generated_sql = get_gemini_response(question=question, prompt=prompt)
            print("\n SQL Query:", generated_sql)

            # Replace specific course names for clarity
            replacements = {
                "CourseName = 'Data Science'": "CourseName = 'Introduction to Data Science'",
                "CourseName = 'Web Development'": "CourseName = 'Web Development Basics'",
                "CourseName = 'Mern Stack'": "CourseName = 'Mern Stack Development'",
                "CourseName = 'Cyber Security'": "CourseName = 'Cyber Security Fundamentals'",
                "CourseName = 'Machine Learning'": "CourseName = 'Machine Learning Concepts'",
                "CourseName = 'Advanced Data Science'": "CourseName = 'Advanced Data Science'",
                "CourseName = 'Full-Stack Development'": "CourseName = 'Full-Stack Development'",
                "CourseName = 'Ethical Hacking'": "CourseName = 'Ethical Hacking'",
                "CourseName = 'Deep Learning'": "CourseName = 'Deep Learning'",
            }
            for old, new in replacements.items():
                generated_sql = generated_sql.replace(old, new)

            response, column_names = read_sql_query(sql=generated_sql, db="student.db")
            
            if response:
                df = pd.DataFrame(response, columns=column_names)
                st.markdown("<h4 class='result-label'>Your Data Insights:</h4>", unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True)  
            else:
                st.error("No records found or invalid query!")
        else:
            st.warning("Please enter a question before submitting.")
