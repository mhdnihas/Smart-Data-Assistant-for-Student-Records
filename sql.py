import sqlite3


connection=sqlite3.connect("student.db")


cursor=connection.cursor()

# removed old student table
cursor.execute("DROP TABLE IF EXISTS STUDENT")
cursor.execute("DROP TABLE IF EXISTS COURSE")
cursor.execute("DROP TABLE IF EXISTS ENROLLMENT")


student_table_info = """
CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(50),
    Age INT,
    Gender VARCHAR(10),
    Class VARCHAR(50),
    Section VARCHAR(10),
    Place VARCHAR(100),
    DateOfBirth DATE,
    CGPA FLOAT
);
"""

course_table_info = """
CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    CourseName VARCHAR(100),
    Credits FLOAT,
    Semester INT
);
""" 

enrollment_table_info = """
CREATE TABLE Enrollment (
    EnrollmentID INT PRIMARY KEY,
    StudentID INT,
    CourseID INT,
    EnrollmentDate DATE,
    FinalGrade VARCHAR(25),
    Status VARCHAR(20),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);
"""



cursor.execute(student_table_info)
cursor.execute(course_table_info)
cursor.execute(enrollment_table_info)


cursor.execute('''
               INSERT INTO Student (StudentID, Name, Age, Gender, Class, Section, Place, DateOfBirth, CGPA) VALUES
    (1, 'Alice Johnson', 20, 'Female', 'Data Science', 'A', '123 Maple St, City', '2003-04-15', 3.8),
    (2, 'Bob Smith', 21, 'Male', 'Web Development', 'B', '456 Oak Ave, City', '2002-05-22', 3.6),
    (3, 'Charlie Brown', 19, 'Male', 'Mern Stack', 'A', '789 Pine Rd, City', '2004-08-30', 3.9),
    (4, 'Diana Prince', 22, 'Female', 'Cyber Security', 'B', '321 Elm St, City', '2001-12-12', 3.5),
    (5, 'Ethan Hunt', 23, 'Male', 'Machine Learning', 'A', '654 Birch Blvd, City', '2000-11-05', 3.7),
    (6, 'Fiona Green', 20, 'Female', 'Data Science', 'A', '111 Cedar St, City', '2003-03-10', 3.2),
    (7, 'George White', 22, 'Male', 'Web Development', 'B', '222 Walnut St, City', '2001-07-15', 3.4),
    (8, 'Hannah Blue', 21, 'Female', 'Cyber Security', 'B', '333 Spruce St, City', '2002-01-25', 3.9),
    (9, 'Ian Black', 24, 'Male', 'Mern Stack', 'C', '444 Fir St, City', '1999-09-05', 2.8),
    (10, 'Judy Red', 23, 'Female', 'Machine Learning', 'C', '555 Ash St, City', '2000-02-20', 3.0);


               ''')

cursor.execute('''
              INSERT INTO Course (CourseID, CourseName, Credits, Semester) VALUES
    (1, 'Introduction to Data Science', 3.0, 1),
    (2, 'Web Development Basics', 4.0, 1),
    (3, 'Mern Stack Development', 4.0, 2),
    (4, 'Cyber Security Fundamentals', 3.0, 1),
    (5, 'Machine Learning Concepts', 3.0, 2),
    (6, 'Advanced Data Science', 3.0, 3),
    (7, 'Full-Stack Development', 4.0, 3),
    (8, 'Ethical Hacking', 3.0, 4),
    (9, 'Deep Learning', 3.0, 3),
    (10, 'AI and ML Integration', 3.0, 4);
            ''')


cursor.execute('''
            INSERT INTO Enrollment (EnrollmentID, StudentID, CourseID, EnrollmentDate, FinalGrade, Status) VALUES
    (1, 1, 1, '2023-09-01', 'A', 'Completed'),
    (2, 2, 2, '2023-09-02', 'B+', 'Completed'),
    (3, 3, 3, '2023-09-01', 'A-', 'Completed'),
    (4, 4, 4, '2023-09-03', 'B+', 'Completed'),
    (5, 5, 5, '2023-09-04', 'C', 'In Progress'),
    (6, 6, 1, '2023-09-05', 'B-', 'Dropped'),
    (7, 7, 2, '2023-09-06', 'A', 'Pending'),
    (8, 8, 8, '2023-09-07', 'B', 'Completed'),
    (9, 9, 3, '2023-09-08', 'F', 'Failed'),
    (10, 10, 9, '2023-09-09', 'C+', 'In Progress');
''')



print('\nStudent table:\n')
data=cursor.execute('Select * from Enrollment')


for row in data:
    print(row)

print('\n Course table:\n')
data=cursor.execute('Select * from COURSE')

for row in data:
    print(row)


print('\n Enrollment table:\n')
data=cursor.execute('Select * from Enrollment')



print('\nStudent details who completed their status in enrollment\n')
data=cursor.execute('Select * from student where studentid in (select studentid from enrollment where status="Completed")')

for row in data:
    print(row)

## close the connection 
connection.commit()
connection.close()