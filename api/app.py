import os
import sys

# Add root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import after path setup
from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import Database, Student, Course, Instructor, Enrollment
from queries import QueryOperations

# Create Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database and models
db = Database()
student_model = Student(db)
course_model = Course(db)
instructor_model = Instructor(db)
enrollment_model = Enrollment(db)
query_ops = QueryOperations(db)

# Routes (copy all routes from main.py)
@app.route('/')
def dashboard():
    """Main dashboard with overview"""
    try:
        # Get statistics
        total_students = len(student_model.find_all())
        total_courses = len(course_model.find_all())
        total_instructors = len(instructor_model.find_all())
        
        # Get all enrollments correctly
        all_students = student_model.find_all()
        total_enrollments = 0
        for student in all_students:
            total_enrollments += len(enrollment_model.find_by_student(student['student_id']))
        
        # Get basic analytics
        avg_gpa_by_major = query_ops.get_average_gpa_by_major()
        top_students = query_ops.get_top_performing_students(5)
        
        return render_template('core/dashboard.html',
                             total_students=total_students,
                             total_courses=total_courses,
                             total_instructors=total_instructors,
                             total_enrollments=total_enrollments,
                             avg_gpa_by_major=avg_gpa_by_major,
                             top_students=top_students)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('core/dashboard.html')

# Add all other routes from main.py here...

# Vercel serverless function handler
def handler(request):
    return app(request.environ, start_response=lambda status, headers: None)

# For local testing
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
