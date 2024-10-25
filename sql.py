import sqlite3


connection=sqlite3.connect("student.db")


cursor=connection.cursor()

# removed old student table
cursor.execute("DROP TABLE IF EXISTS STUDENT")


table_info="""
Create Table STUDENT(NAME VARCHAR(25),AGE INT,GENDER VARCHAR(10),CLASS VARCHAR(25),SECTION VARCHAR(25) , MARKS INT);
"""

cursor.execute(table_info)


cursor.execute('''Insert into STUDENT values('Muhammed Nihas',22,'MALE','Data Science','A',100)''')
cursor.execute('''Insert into STUDENT values('Muhammed Zayid',19,'MALE','Mern Stack','A',100)''')
cursor.execute('''Insert into STUDENT values('Nihala Sherin',23,'FEMALE','Python Django','B',55)''')
cursor.execute('''Insert into STUDENT values('Fathima Najla',20,'FEMALE','Flutter','A',60)''')
cursor.execute('''Insert into STUDENT values('Muhammed KM',23,'MALE','Python Django','B',95)''')
cursor.execute('''Insert into STUDENT values('Vinil',22,'MALE','Data Science','A',85)''')
cursor.execute('''Insert into STUDENT values('Ahmad Rafi',23,'MALE','Cyber Security','A',50)''')
cursor.execute('''Insert into STUDENT values('Ali',19,'MALE','Mern Stack','A',60)''')
cursor.execute('''Insert into STUDENT values('Shadin',19,'MALE','Flutter','B',65)''')
cursor.execute('''Insert into STUDENT values('Shabeer Ali',25,'MALE','Mern Stack','A',45)''')




print('The inserted Records are :')

data=cursor.execute('Select * from STUDENT')


for row in data:
    print(row)


## close the connection 
connection.commit()
connection.close()