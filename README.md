Educational Courses Management System
This is a simple Educational Courses Management System implemented using Flask, MySQL, and FPDF. The system allows users to register, log in, view registered courses, and download transcripts with grades.

Setup
Prerequisites
Python 3.x
Flask
Flask-MySQLdb
FPDF
Installation
Install the required dependencies:

bash
Copy code
pip install Flask Flask-MySQLdb fpdf
Configure MySQL settings in the code:

python
Copy code
# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '110881'
app.config['MYSQL_DB'] = 'educational_courses_db'
Create the database and tables by running the application once:

bash
Copy code
python your_app_name.py
(Comment out or remove the create_database() and create_tables() functions once the database is created to avoid errors on subsequent runs.)

Optionally, insert sample data to test the application:

python
Copy code
# Run the function to insert sample data
insert_sample_data()
Usage
Run the application:

bash
Copy code
python your_app_name.py
Access the application at http://localhost:5000 in your web browser.

Features
User Registration: Users can register by providing their details such as first name, last name, age, username, and password.

User Login: Registered users can log in using their username and password.

User Panel: After logging in, users can view the courses they are registered for.

Transcript Download: Users can download their transcripts for specific courses, which include grades for respective exams.

Routes
/register: User registration page.
/login: User login page.
/user_panel: User panel displaying registered courses.
/download_transcript/<int:course_id>: Download transcript for a specific course.
Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

License
This project is licensed under the MIT License.
