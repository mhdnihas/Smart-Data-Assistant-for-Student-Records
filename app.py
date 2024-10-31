from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import sqlite3
import pandas as pd



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
    return rows,column_names

# Prompt for Gemini model
prompt = ["""
    You are an SQL expert converting English questions into SQL queries. The database contains three tables:

    Student table with columns: StudentID, Name, Age, Gender, Class, Section, Place, DateOfBirth, and CGPA.
    Course table with columns: CourseID, CourseName, Credits, and Semester.
    Enrollment table with columns: EnrollmentID, StudentID, CourseID, EnrollmentDate, FinalGrade, and Status.
         course enrollments, grades, and statuses.
    Given a question, Write SQL queries to retrieve information from the SQLite database.  To support the database structure, use partial matching with the LIKE clause when searching course names, rather than exact matches. For example, if asked for "Data Science" or "Python Django" courses, look for course names containing "Data Science" or "Python" using LIKE statements.
    Ensure the queries are correctly formatted, contain no comments, and do not include any code block markers.
    also the sql code should not have ``` in beginning or end and sql word in output


"""]



st.set_page_config(page_title="Ask Anything: Instantly Retrieve Insights from Student Records", page_icon="🤖", layout="centered")

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
st.sidebar.write("- Find the second highest scoring student in 'Data Science' or 'Python Django ?")


with st.container():
    st.markdown("<h1 class='title-text'>Effortlessly Turn Your Questions Into Actionable Data</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='sub-header'>Ask your questions, and get the data you need!</h4>", unsafe_allow_html=True)


    st.markdown("<h4 class='input-label'>Enter your question about the student database:</h4>", unsafe_allow_html=True)

    question = st.text_input(
    label="Question", 
    placeholder="E.g., How many students are in Data Science?",
    key='input',
    label_visibility="hidden"  )
    
    submit = st.button("Show Results")


    if submit:
        if question:
            generated_sql = get_gemini_response(question=question, prompt=prompt)
            print("\n SQL Quary:",generated_sql)

            generated_sql = generated_sql.replace("CourseName = 'Data Science'", "CourseName = 'Introduction to Data Science'")
            generated_sql = generated_sql.replace("CourseName = 'Web Development'", "CourseName = 'Web Development Basics'")
            generated_sql = generated_sql.replace("CourseName = 'Mern Stack'", "CourseName = 'Mern Stack Development'")
            generated_sql = generated_sql.replace("CourseName = 'Cyber Security'", "CourseName = 'Cyber Security Fundamentals'")
            generated_sql = generated_sql.replace("CourseName = 'Machine Learning'", "CourseName = 'Machine Learning Concepts'")
            generated_sql = generated_sql.replace("CourseName = 'Data Science'", "CourseName = 'Advanced Data Science'")
            generated_sql = generated_sql.replace("CourseName = 'Web Development'", "CourseName = 'Full-Stack Development'")
            generated_sql = generated_sql.replace("CourseName = 'Cyber Security'", "CourseName = 'Ethical Hacking'")
            generated_sql = generated_sql.replace("CourseName = 'Machine Learning'", "CourseName = 'Deep Learning'")
            generated_sql = generated_sql.replace("CourseName = 'AI and ML Integration'", "CourseName = 'Deep Learning'")



            response,column_names = read_sql_query(sql=generated_sql , db="student.db")
            
            if response:
                df = pd.DataFrame(response, columns=column_names)
                st.markdown("<h4 class='result-label'>Your Data Insights:</h4>", unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True)  
            else:
                st.error("No records found or invalid query!")
        else:
            st.warning("Please enter a question before submitting.")
