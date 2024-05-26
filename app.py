import os
import time

from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
import csv

app = Flask(__name__)


# Function to read CSV file
def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data


# Function to write to CSV file
def write_csv(filename, data):
    with open(filename, 'w', newline='') as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# Function to add new user to CSV file
def add_user_to_csv(username, password, category, email):
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, category, email])
        print("added")


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check credentials
        # Redirect to dashboard or display error message
        pass
    return render_template('login.html')


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        category = request.form['category']
        email = request.form['email']

        # Add new user to CSV file
        add_user_to_csv(username, password, category, email)
        pass

    return render_template('register.html')


# coach management routes (add, delete, update)
@app.route('/coaches')
def coachs():
    coachs_data = read_csv('coaches.csv')
    return render_template('coaches.html', coachs=coachs_data)


# File upload route

# Function to handle file upload
def upload_file(file):
    # Specify the directory where you want to store uploaded files
    upload_dir = 'backend/static/html'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)
    return file_path


# Route to display file upload form
@app.route('/upload')
def upload_form():
    return render_template('upload.html')


# Route to handle file upload
@app.route('/upload_file', methods=['POST'])
def upload_file_route():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = upload_file(file)
        return f'File uploaded successfully! Path: {file_path}'
    return redirect(url_for('upload_form'))


# File download route
@app.route('/download/<filename>')
def download(filename):
    # Handle file download
    pass


# Function to read courses from CSV file
def read_courses():
    with open('courses.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        courses = list(reader)
    return courses


# Function to write courses to CSV file
def write_courses(courses):
    with open('courses.csv', 'a', newline='') as file:
        fieldnames = ['id', 'name', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(courses)


# Route to display courses
@app.route('/courses')
def courses():
    courses = read_courses()
    return render_template('courses.html', courses=courses)


# Route to add a new course
@app.route('/add_course', methods=['POST'])
def add_course():
    courses = read_courses()
    course_id = len(courses) + 1
    course_name = request.form['course_name']
    description = request.form['description']
    new_course = {'id': course_id, 'name': course_name, 'description': description}
    courses.append(new_course)
    write_courses(courses)
    return redirect(url_for('courses'))


# Route to update a course
@app.route('/update_course/<int:course_id>')
def update_course(course_id):
    courses = read_courses()
    # Code to update the course based on the course_id
    return redirect(url_for('courses'))


# Route to delete a course
@app.route('/delete_course/<int:course_id>')
def delete_course(course_id):
    courses = read_courses()
    # Code to delete the course based on the course_id
    return redirect(url_for('courses'))

def generate_html(directory):
    # List HTML files in the directory
    html_files = [file for file in os.listdir(directory) if file.endswith('.html')]

    # Generate HTML content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTML File List</title>
    </head>
    <body>
        <h1>HTML File List</h1>
        <ul>
    """
    for file in html_files:
        html_content += f'<li><a href="static/html/{file}">{file}</a></li>'

    html_content += """
        </ul>
    </body>
    </html>
    """

    # Write HTML content to a file
    with open('backend/templates/file_list.html', 'w') as html_file:
        html_file.write(html_content)

# Call the generate_html function with the directory path
generate_html('backend/static/html')  # Replace 'your_directory_path' with the path to your directory

# Function to list files in a directory
def list_files(directory):
    files = os.listdir(directory)
    return files

# Route to render the file list template
@app.route('/view')
def file_list():
    generate_html('backend/static/html')
    return render_template('file_list.html')


# Route to load HTML files
@app.route('/html/<filename>')
def html_files(filename):
    #return render_template(filename)
    return send_from_directory('static/html', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
