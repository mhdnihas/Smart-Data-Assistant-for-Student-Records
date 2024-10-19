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

