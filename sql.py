import sqlite3


connection=sqlite3.connect("student.db")


cursor=connection.cursor()

table_info="""
Create Table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25) , MARKS INT);
"""

cursor.execute(table_info)


cursor.execute('''Insert into STUDENT values('Muhammed Nihas','Data Science','A',90)''')
cursor.execute('''Insert into STUDENT values('Muhammed Zayid','Mern Stack','A',100)''')
cursor.execute('''Insert into STUDENT values('Muhammed KM','Python Django','B',95)''')
cursor.execute('''Insert into STUDENT values('Vinil','Data Science','A',85)''')
cursor.execute('''Insert into STUDENT values('Ahmad Rafi','Cyber Security','A',50)''')
cursor.execute('''Insert into STUDENT values('Ali','Mern Stack','A',60)''')



print('The inserted Records are :')

data=cursor.execute('Select * from STUDENT')


for row in data:
    print(row)


## close the connection 
connection.commit()
connection.close()