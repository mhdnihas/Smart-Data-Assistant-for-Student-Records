from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai 
import os
import sqlite3


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) 


def get_gemini_response(question,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content([prompt[0],question])
    return response.text


def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()

    for row in rows:
        print(row)

    return row


prompt=["""
        Your are the expert in converting English question to SQL query !
        The SQL Database has the student table and which have following columns -NAME , CLASS , SECTION , MARKS .\n \n 
        For example , example 1 - How many entries of records are present ? , the SQL query something like this select * from student ; 
        example 2 - who are studying Mearnstack ? the SQL query something like this select * from student where CLASS="Mern Stack";
        """]

st.set_page_config(page_title="I can Retrieve Any SQL query")

st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input:",key='input')

submit = st.button("Ask the question")


if submit:

    sql_query=get_gemini_response(question=question,prompt=prompt)
    print("SQL qeurty:",sql_query)
    response=read_sql_query(sql=sql_query,db="student.db")
    
    st.subheader("Response is ...")
    for row in response:
        print(row)
        st.header(row)
