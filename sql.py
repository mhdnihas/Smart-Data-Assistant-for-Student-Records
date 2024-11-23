import sqlite3
import pandas as pd

# Establish a connection to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('student.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS STUDENT")
cursor.execute("DROP TABLE IF EXISTS COURSE")
cursor.execute("DROP TABLE IF EXISTS ENROLLMENT")


# 1. Create Student Table

student_df = pd.read_csv('data/students.csv')
course_df = pd.read_csv('data/courses.csv')
enrollment_df = pd.read_csv('data/enrollment_table.csv')

# Write data to the database (Pandas will create tables automatically)
student_df.to_sql('Student', conn, if_exists='replace', index=False)
course_df.to_sql('Course', conn, if_exists='replace', index=False)
enrollment_df.to_sql('Enrollment', conn, if_exists='replace', index=False)


print("TotalStudents:")
for row in cursor.execute("""SELECT 
        s.StudentID,
        s.Name,
        c.CourseName,
        c.Department,
        e.Grade
    FROM 
        Enrollment e
    JOIN 
        Student s ON e.StudentID = s.StudentID
    JOIN 
        Course c ON e.CourseID = c.CourseID
    LIMIT 10;
    """).fetchall():
    print(row)

print("\nCount the Number of Enrollments per Course:")
for row in cursor.execute("""SELECT 
            c.CourseName,
            COUNT(e.EnrollmentID) AS TotalEnrollments
        FROM 
            Course c
        JOIN 
            Enrollment e ON c.CourseID = e.CourseID
        GROUP BY 
            c.CourseName
        ORDER BY 
            TotalEnrollments DESC;
        """).fetchall():
    print(row)

print("\n\nAverage Grade by Course:")
for row in cursor.execute("""
        SELECT c.CourseName,
            AVG(CASE 
                WHEN e.Grade = 'A' THEN 4
                WHEN e.Grade = 'B' THEN 3
                WHEN e.Grade = 'C' THEN 2
                WHEN e.Grade = 'D' THEN 1
                ELSE 0 END) AS AverageGrade
        FROM 
            Enrollment e
        JOIN 
            Course c ON e.CourseID = c.CourseID
        GROUP BY 
            c.CourseName
        ORDER BY 
            AverageGrade DESC;
        """).fetchall():
    print(row)


# Commit the insertions
conn.commit()

# Close the connection
conn.close()

print("Data successfully imported into student.db")
