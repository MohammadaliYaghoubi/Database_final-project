from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_mysqldb import MySQL
import os
from fpdf import FPDF
import secrets
import datetime

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '110881'
app.config['MYSQL_DB'] = 'educational_courses_db'

mysql = MySQL(app)

# Create the database and select it
def create_database():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('CREATE DATABASE IF NOT EXISTS educational_courses_db')
        cur.execute('USE educational_courses_db')  # Select the created database
        mysql.connection.commit()
        cur.close()

# Create tables
def create_tables():
    with app.app_context():
        cur = mysql.connection.cursor()

        # Courses table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL
            )
        ''')

        # Subsections table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS subsections (
                id INT PRIMARY KEY AUTO_INCREMENT,
                course_id INT,
                name VARCHAR(255) NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(id)
            )
        ''')

        # Exams table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS exams (
                id INT PRIMARY KEY AUTO_INCREMENT,
                subsection_id INT,
                name VARCHAR(255) NOT NULL,
                FOREIGN KEY (subsection_id) REFERENCES subsections(id)
            )
        ''')

        # Students table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INT PRIMARY KEY AUTO_INCREMENT,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                age INT NOT NULL,
                username VARCHAR(255) UNIQUE NOT NULL,
                password INT NOT NULL
            )
        ''')

        # Students_Courses table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS students_courses (
                id INT PRIMARY KEY AUTO_INCREMENT,
                student_id INT,
                course_id INT,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (course_id) REFERENCES courses(id)
            )
        ''')

        # Grades table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INT PRIMARY KEY AUTO_INCREMENT,
                student_id INT,
                exam_id INT,
                grade INT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (exam_id) REFERENCES exams(id)
            )
        ''')
        mysql.connection.commit()
        cur.close()

# Run the functions to create the database and tables
create_database()
create_tables()

# Function to insert sample data
def insert_sample_data():
    with app.app_context():
        cur = mysql.connection.cursor()

        try:
            # Insert sample courses
            cur.execute("INSERT INTO courses (name, start_date, end_date) VALUES ('Python Course', '2023-01-01', '2023-03-01')")
                        
            cur.execute("INSERT INTO courses (name, start_date, end_date) VALUES ('Web Development Course', '2023-02-01', '2023-04-01')")

            # Insert sample subsections
            cur.execute("INSERT INTO subsections (course_id, name) VALUES (1, 'Python Basics')")

            cur.execute("INSERT INTO subsections (course_id, name) VALUES (1, 'Advanced Python')")
            
            cur.execute("INSERT INTO subsections (course_id, name) VALUES (1, 'Database')")
            
            cur.execute("INSERT INTO subsections (course_id, name) VALUES (2, 'HTML/CSS')")
            
            cur.execute("INSERT INTO subsections (course_id, name) VALUES (2, 'JavaScript')")

            # Insert sample exams
            cur.execute("INSERT INTO exams (subsection_id, name) VALUES (1, 'Conditions')")

            cur.execute("INSERT INTO exams (subsection_id, name) VALUES (1, 'Loops')")

            cur.execute("INSERT INTO exams (subsection_id, name) VALUES (2, 'Python Decorators')")

            cur.execute("INSERT INTO exams (subsection_id, name) VALUES (4, 'HTML Basics')")

            cur.execute("INSERT INTO exams (subsection_id, name) VALUES (5, 'JavaScript Functions')")

            # Insert sample students
            cur.execute("INSERT INTO students (first_name, last_name, age, username, password) VALUES ('Aria', 'Yaghoubi', 21, 'aria', '123')")

            cur.execute("INSERT INTO students (first_name, last_name, age, username, password) VALUES ('Pejman', 'Javid', 22, 'pejman', '456')")

            # Insert sample student_courses
            cur.execute("INSERT INTO students_courses (student_id, course_id) VALUES (1, 1)")

            cur.execute("INSERT INTO students_courses (student_id, course_id) VALUES (1, 2)")

            cur.execute("INSERT INTO students_courses (student_id, course_id) VALUES (2, 1)")

            # Insert sample grades
            cur.execute("INSERT INTO grades (student_id, exam_id, grade) VALUES (1, 1, 90)")

            cur.execute("INSERT INTO grades (student_id, exam_id, grade) VALUES (1, 2, 85)")

            cur.execute("INSERT INTO grades (student_id, exam_id, grade) VALUES (2, 1, 92)")

            cur.execute("INSERT INTO grades (student_id, exam_id, grade) VALUES (2, 3, 88)")

            mysql.connection.commit()
        except Exception as e:
            # Log the error or print it for debugging purposes
            print(f"Error inserting data: {e}")
            # Optionally, you can rollback the transaction to avoid partially inserting data
            mysql.connection.rollback()
        finally:
            cur.close()       

# Run the function to insert sample data
insert_sample_data()

# User Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (first_name, last_name, age, username, password) VALUES (%s, %s, %s, %s, %s)",
                    (first_name, last_name, age, username, password))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('register.html')


# User Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # Assuming user ID is the first element in the tuple
            session['user_id'] = user[0]
            return redirect(url_for('user_panel'))

    return render_template('login.html')



# User Panel Route
@app.route('/user_panel')
def user_panel():
    if 'user_id' in session:
        user_id = session['user_id']

        # Fetch user's registered courses
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM courses WHERE id IN (SELECT course_id FROM students_courses WHERE student_id = %s)", (user_id,))
        courses = cur.fetchall()
        cur.close()

        return render_template('user_panel.html', courses=courses)

    return redirect(url_for('login'))

# Download Transcript Route
@app.route('/download_transcript/<int:course_id>')
def download_transcript(course_id):
    if 'user_id' in session:
        user_id = session['user_id']

        # Fetch user's grades for the selected course
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM grades WHERE student_id = %s AND exam_id IN (SELECT id FROM exams WHERE subsection_id IN (SELECT id FROM subsections WHERE course_id = %s))",
                    (user_id, course_id))
        grades = cur.fetchall()
        cur.close()

        # Create PDF transcript
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Transcript", ln=True, align='C')
        pdf.ln(10)

        for grade in grades:
            pdf.cell(50, 10, txt=f"Exercise {grade['id']}", ln=True)
            pdf.cell(50, 10, txt=f"Grade: {grade['grade']}", ln=True)

        transcript_filename = f"transcript_course_{course_id}_user_{user_id}.pdf"
        transcript_filepath = os.path.join(app.root_path, 'static', transcript_filename)
        pdf.output(transcript_filepath)

        return send_file(transcript_filepath, as_attachment=True)

    return redirect(url_for('login'))

# Home Page Route
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.secret_key = '110881' 
    app.run(debug=True)
