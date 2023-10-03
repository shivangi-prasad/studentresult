from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

#connect to db
con = psycopg2.connect(
    host = "127.0.0.1",
    database = "Student Result System",
    user = "postgres",
    password = "*Shivangi123"
)

cur = con.cursor()

cur.execute("select * from public.Subjects")
# SQL query with corrected syntax for inserting data into the "department" table
insert_query = """
    INSERT INTO public.department ("DeptId", "DepartmentName", "StudentId")
    VALUES (%s, %s, %s)
"""

# Data to be inserted
# data = (6, 'HSS', 3)

# cur.execute(insert_query, data)

con.commit()

rows = cur.fetchall()

for r in rows:
    print (f"DeptId {r[0]} DepartmentName {r[1]} StudentId {r[2]} ")

cur.close


#close the connection
con.close()