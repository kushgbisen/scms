from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import Database, Student, Course, Instructor, Enrollment
from queries import QueryOperations
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Setup database
db = Database()
student_model = Student(db)
course_model = Course(db)
instructor_model = Instructor(db)
enrollment_model = Enrollment(db)
query_ops = QueryOperations(db)

# Routes
@app.route('/')
def dashboard():
    """Dashboard home"""
    try:
        # Get stats
        total_students = len(student_model.find_all())
        total_courses = len(course_model.find_all())
        total_instructors = len(instructor_model.find_all())
        
        # Count enrollments
        all_students = student_model.find_all()
        total_enrollments = 0
        for student in all_students:
            total_enrollments += len(enrollment_model.find_by_student(student['student_id']))
        
        # Get analytics
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

# Students
@app.route('/students')
def students_list():
    """Student list with filters"""
    try:
        # Get filters
        major = request.args.get('major')
        year = request.args.get('year')
        min_gpa = request.args.get('min_gpa')
        max_gpa = request.args.get('max_gpa')
        
        students = []
        if major or year or min_gpa or max_gpa:
            # Filter if needed
            students = query_ops.filter_students(
                major=major,
                year=year,
                min_gpa=min_gpa,
                max_gpa=max_gpa
            )
        else:
            # Get all
            students = student_model.find_all()
        
        # Filter options
        available_majors = query_ops.get_available_majors()
        available_years = query_ops.get_available_years()
        
        return render_template('lists/students_list.html', 
                             students=students,
                             available_majors=available_majors,
                             available_years=available_years,
                             current_filters={
                                 'major': major,
                                 'year': year,
                                 'min_gpa': min_gpa,
                                 'max_gpa': max_gpa
                             })
    except Exception as e:
        flash(f'Error loading students: {str(e)}', 'error')
        # Provide all vars for error
        return render_template('lists/students_list.html', 
                             students=[],
                             available_majors=[],
                             available_years=[],
                             current_filters={
                                 'major': '',
                                 'year': '',
                                 'min_gpa': '',
                                 'max_gpa': ''
                             })

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    """Add student"""
    if request.method == 'POST':
        try:
            student_data = {
                "student_id": request.form['student_id'],
                "name": {
                    "first": request.form['first_name'],
                    "last": request.form['last_name']
                },
                "email": request.form['email'],
                "major": request.form['major'],
                "year": request.form['year'],
                "gpa": float(request.form['gpa'])
            }
            student_model.create(student_data)
            flash('Student added successfully!', 'success')
            return redirect(url_for('students_list'))
        except Exception as e:
            flash(f'Error adding student: {str(e)}', 'error')
    
    return render_template('forms/student_form.html', title="Add Student")

@app.route('/students/<student_id>')
def view_student(student_id):
    """View student"""
    try:
        student = student_model.find_by_id(student_id)
        if student:
            enrollments = enrollment_model.find_by_student(student_id)
            return render_template('lists/student_detail.html', student=student, enrollments=enrollments, student_model=student_model, course_model=course_model)
        else:
            flash('Student not found!', 'error')
            return redirect(url_for('students_list'))
    except Exception as e:
        flash(f'Error viewing student: {str(e)}', 'error')
        return redirect(url_for('students_list'))

@app.route('/students/<student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    """Edit student"""
    try:
        student = student_model.find_by_id(student_id)
        if not student:
            flash('Student not found!', 'error')
            return redirect(url_for('students_list'))
        
        if request.method == 'POST':
            update_data = {
                "name.first": request.form['first_name'],
                "name.last": request.form['last_name'],
                "email": request.form['email'],
                "major": request.form['major'],
                "year": request.form['year'],
                "gpa": float(request.form['gpa'])
            }
            student_model.update(student_id, update_data)
            flash('Student updated successfully!', 'success')
            return redirect(url_for('view_student', student_id=student_id))
        
        return render_template('forms/student_form.html', title="Edit Student", student=student)
    except Exception as e:
        flash(f'Error editing student: {str(e)}', 'error')
        return redirect(url_for('students_list'))

@app.route('/students/<student_id>/delete', methods=['POST'])
def delete_student(student_id):
    """Delete student"""
    try:
        student_model.delete(student_id)
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'error')
    return redirect(url_for('students_list'))

# Courses
@app.route('/courses')
def courses_list():
    """Course list with filters"""
    try:
        # Get filter parameters
        instructor_id = request.args.get('instructor_id')
        credits = request.args.get('credits')
        semester = request.args.get('semester')
        year = request.args.get('year')
        
        courses = []
        if instructor_id or credits or semester or year:
            # Apply filters
            courses = query_ops.filter_courses(
                instructor_id=instructor_id,
                credits=credits,
                semester=semester,
                year=year
            )
        else:
            # Get all courses
            courses = course_model.find_all()
        
        # Get filter options
        available_instructors = instructor_model.find_all()
        available_credits = query_ops.get_available_credits()
        available_semesters = query_ops.get_available_semesters()
        
        return render_template('lists/courses_list.html', 
                             courses=courses,
                             available_instructors=available_instructors,
                             available_credits=available_credits,
                             available_semesters=available_semesters,
                             current_filters={
                                 'instructor_id': instructor_id,
                                 'credits': credits,
                                 'semester': semester,
                                 'year': year
                             })
    except Exception as e:
        flash(f'Error loading courses: {str(e)}', 'error')
        # Provide all vars for error
        return render_template('lists/courses_list.html', 
                             courses=[],
                             available_instructors=[],
                             available_credits=[],
                             available_semesters=[],
                             current_filters={
                                 'instructor_id': '',
                                 'credits': '',
                                 'semester': '',
                                 'year': ''
                             })

@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    """Add course"""
    if request.method == 'POST':
        try:
            prerequisites = [p.strip() for p in request.form.get('prerequisites', '').split(',') if p.strip()]
            course_data = {
                "course_code": request.form['course_code'],
                "title": request.form['title'],
                "description": request.form['description'],
                "credits": int(request.form['credits']),
                "instructor_id": request.form['instructor_id'],
                "semester": request.form['semester'],
                "year": int(request.form['year']),
                "prerequisites": prerequisites
            }
            course_model.create(course_data)
            flash('Course added successfully!', 'success')
            return redirect(url_for('courses_list'))
        except Exception as e:
            flash(f'Error adding course: {str(e)}', 'error')
    
    instructors = instructor_model.find_all()
    return render_template('forms/course_form.html', title="Add Course", instructors=instructors)

@app.route('/courses/<course_code>')
def view_course(course_code):
    """View course"""
    try:
        course = course_model.find_by_code(course_code)
        if course:
            enrollments = enrollment_model.find_by_course(course_code)
            return render_template('lists/course_detail.html', course=course, enrollments=enrollments, student_model=student_model, instructor_model=instructor_model, enrollment_model=enrollment_model)
        else:
            flash('Course not found!', 'error')
            return redirect(url_for('courses_list'))
    except Exception as e:
        flash(f'Error viewing course: {str(e)}', 'error')
        return redirect(url_for('courses_list'))

@app.route('/courses/<course_code>/edit', methods=['GET', 'POST'])
def edit_course(course_code):
    """Edit course"""
    try:
        course = course_model.find_by_code(course_code)
        if not course:
            flash('Course not found!', 'error')
            return redirect(url_for('courses_list'))
        
        if request.method == 'POST':
            prerequisites = [p.strip() for p in request.form.get('prerequisites', '').split(',') if p.strip()]
            update_data = {
                "title": request.form['title'],
                "description": request.form['description'],
                "credits": int(request.form['credits']),
                "instructor_id": request.form['instructor_id'],
                "semester": request.form['semester'],
                "year": int(request.form['year']),
                "prerequisites": prerequisites
            }
            course_model.update(course_code, update_data)
            flash('Course updated successfully!', 'success')
            return redirect(url_for('view_course', course_code=course_code))
        
        instructors = instructor_model.find_all()
        return render_template('forms/course_form.html', title="Edit Course", course=course, instructors=instructors)
    except Exception as e:
        flash(f'Error editing course: {str(e)}', 'error')
        return redirect(url_for('courses_list'))

@app.route('/courses/<course_code>/delete', methods=['POST'])
def delete_course(course_code):
    """Delete course"""
    try:
        course_model.delete(course_code)
        flash('Course deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting course: {str(e)}', 'error')
    return redirect(url_for('courses_list'))

# Instructors
@app.route('/instructors')
def instructors_list():
    """Instructor list with filters"""
    try:
        # Get filter parameters
        department = request.args.get('department')
        
        instructors = []
        if department:
            # Apply filters
            instructors = query_ops.filter_instructors(department=department)
        else:
            # Get all instructors
            instructors = instructor_model.find_all()
        
        # Get filter options
        available_departments = query_ops.get_available_departments()
        
        return render_template('lists/instructors_list.html', 
                             instructors=instructors,
                             available_departments=available_departments,
                             current_filters={
                                 'department': department
                             })
    except Exception as e:
        flash(f'Error loading instructors: {str(e)}', 'error')
        # Provide all vars for error
        return render_template('lists/instructors_list.html', 
                             instructors=[],
                             available_departments=[],
                             current_filters={
                                 'department': ''
                             })

@app.route('/instructors/add', methods=['GET', 'POST'])
def add_instructor():
    """Add instructor"""
    if request.method == 'POST':
        try:
            instructor_data = {
                "instructor_id": request.form['instructor_id'],
                "name": {
                    "first": request.form['first_name'],
                    "last": request.form['last_name']
                },
                "email": request.form['email'],
                "department": request.form['department']
            }
            instructor_model.create(instructor_data)
            flash('Instructor added successfully!', 'success')
            return redirect(url_for('instructors_list'))
        except Exception as e:
            flash(f'Error adding instructor: {str(e)}', 'error')
    
    return render_template('forms/instructor_form.html', title="Add Instructor")

@app.route('/instructors/<instructor_id>')
def view_instructor(instructor_id):
    """View instructor"""
    try:
        instructor = instructor_model.find_by_id(instructor_id)
        if instructor:
            courses = query_ops.find_courses_by_instructor(instructor_id)
            return render_template('lists/instructor_detail.html', instructor=instructor, courses=courses, enrollment_model=enrollment_model)
        else:
            flash('Instructor not found!', 'error')
            return redirect(url_for('instructors_list'))
    except Exception as e:
        flash(f'Error viewing instructor: {str(e)}', 'error')
        return redirect(url_for('instructors_list'))

@app.route('/instructors/<instructor_id>/edit', methods=['GET', 'POST'])
def edit_instructor(instructor_id):
    """Edit instructor"""
    try:
        instructor = instructor_model.find_by_id(instructor_id)
        if not instructor:
            flash('Instructor not found!', 'error')
            return redirect(url_for('instructors_list'))
        
        if request.method == 'POST':
            update_data = {
                "name.first": request.form['first_name'],
                "name.last": request.form['last_name'],
                "email": request.form['email'],
                "department": request.form['department']
            }
            
            updated_count = instructor_model.update(instructor_id, update_data)
            if updated_count > 0:
                flash('Instructor updated successfully!', 'success')
            else:
                flash('No changes made to instructor.', 'success')
            return redirect(url_for('view_instructor', instructor_id=instructor_id))
        
        return render_template('forms/instructor_form.html', title="Edit Instructor", instructor=instructor)
    except Exception as e:
        flash(f'Error editing instructor: {str(e)}', 'error')
        return redirect(url_for('instructors_list'))

@app.route('/instructors/<instructor_id>/delete', methods=['POST'])
def delete_instructor(instructor_id):
    """Delete instructor"""
    try:
        deleted_count = instructor_model.delete(instructor_id)
        if deleted_count > 0:
            flash('Instructor deleted successfully!', 'success')
        else:
            flash('Instructor not found!', 'error')
    except Exception as e:
        flash(f'Error deleting instructor: {str(e)}', 'error')
    return redirect(url_for('instructors_list'))

# Enrollments
@app.route('/enrollments')
def enrollments_list():
    """Enrollment list with filters"""
    try:
        # Get filter parameters
        student_id = request.args.get('student_id')
        course_code = request.args.get('course_code')
        status = request.args.get('status')
        
        # Get filter options
        available_students = student_model.find_all()
        available_courses = course_model.find_all()
        available_statuses = ['Active', 'Completed', 'Dropped', 'Withdrawn']
        
        # Pre-load data for template
        students_dict = {}
        for student in available_students:
            students_dict[student['student_id']] = student
            
        courses_dict = {}  
        for course in available_courses:
            courses_dict[course['course_code']] = course
        
        enrollments = []
        if student_id or course_code or status:
            # Apply filters
            enrollments = query_ops.filter_enrollments(
                student_id=student_id,
                course_code=course_code,
                status=status
            )
        else:
            # Get enrollments fast
            enrollments = enrollment_model.collection.find({}).sort([("created_at", -1)])
            enrollments = list(enrollments)
        
        return render_template('lists/enrollments_list.html', 
                             enrollments=enrollments,
                             available_students=available_students,
                             available_courses=available_courses,
                             available_statuses=available_statuses,
                             current_filters={
                                 'student_id': student_id,
                                 'course_code': course_code,
                                 'status': status
                             },
                             students_dict=students_dict,
                             courses_dict=courses_dict,
                             student_model=student_model, 
                             course_model=course_model, 
                             instructor_model=instructor_model)
    except Exception as e:
        flash(f'Error loading enrollments: {str(e)}', 'error')
        # Provide all vars for error
        return render_template('lists/enrollments_list.html', 
                             enrollments=[],
                             available_students=[],
                             available_courses=[],
                             available_statuses=[],
                             current_filters={
                                 'student_id': '',
                                 'course_code': '',
                                 'status': ''
                             },
                             students_dict={},
                             courses_dict={},
                             student_model=student_model, 
                             course_model=course_model, 
                             instructor_model=instructor_model)

@app.route('/enrollments/add', methods=['GET', 'POST'])
def add_enrollment():
    """Add enrollment"""
    if request.method == 'POST':
        try:
            enrollment_data = {
                "student_id": request.form['student_id'],
                "course_code": request.form['course_code'],
                "status": request.form['status']
            }
            enrollment_model.create(enrollment_data)
            flash('Enrollment added successfully!', 'success')
            return redirect(url_for('enrollments_list'))
        except Exception as e:
            flash(f'Error adding enrollment: {str(e)}', 'error')
    
    students = student_model.find_all()
    courses = course_model.find_all()
    return render_template('forms/enrollment_form.html', title="Add Enrollment", students=students, courses=courses)

@app.route('/enrollments/delete', methods=['POST'])
def delete_enrollment():
    """Delete enrollment"""
    try:
        student_id = request.form['student_id']
        course_code = request.form['course_code']
        enrollment_model.delete(student_id, course_code)
        flash('Enrollment deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting enrollment: {str(e)}', 'error')
    return redirect(url_for('enrollments_list'))





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
