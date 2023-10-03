from flask import Flask, render_template, request,redirect,url_for, session
from flask_bcrypt import Bcrypt
import psycopg2

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'

# Database connection parameters
db_params = {
    'dbname': 'Student Result System',
    'user': 'postgres',
    'password': '*Shivangi123',
    'host': 'localhost',  # Change this if your database is running on a different host
    'port': '5432',       # Change this if your PostgreSQL port is different
}

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        roll_number = request.form['rollNumber']
        password = request.form['password']

        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Example SQL query to check student login credentials

        # cur.execute("SELECT * FROM student WHERE roll_number = %s", (roll_number,))
        cur.execute("select * from usercredentials WHERE roll_number = %s AND password = %s", (roll_number,password))

        #getting result for that particular roll no and passing it to home page while redirecting 
        user = cur.fetchone()

        #for password 
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        print(hashed_password)
        # is_valid = bcrypt.check_password_hash(hashed_password, password)
        # print(is_valid)

        if user[2] == hashed_password:
            session['loggedin'] = True

        cur.close()
        conn.close()

        if user:
            session['user_data'] = user
            # Authentication successful, redirect to a success page or perform further actions
            return redirect(url_for("home")) # this is my home function
            # return "Login successful! Welcome, " + user[1]  
        else:
            # Authentication failed, redirect to an error page or show an error message
            return "Login failed! Invalid credentials. Please try again."

    # Render the login form for GET requests
    return render_template('index.html')

#this is main home function which is sending mt to url /home and and i am going to home.html
@app.route('/home', methods=['GET', 'POST'])
def home():
    #logic
    user_data = session.get('user_data', None)
    # print(user_data)
    # print(user_data[1])
    connection = psycopg2.connect(**db_params)
    curser = connection.cursor()
    curser.execute("""select * from usercredentials as u 
natural join result as r
natural join student as s
natural join department as d
natural join subjects as sb where u.roll_number = %s""", (user_data[1],))
    result = curser.fetchall()
    print(result)

    curser.close()
    connection.close()
   
    return render_template('home.html', data = result)

if __name__ == '__main__':
    app.run(debug=True)
