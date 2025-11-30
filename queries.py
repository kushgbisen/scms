from pymongo import ASCENDING, DESCENDING
from datetime import datetime

class QueryOperations:
    def __init__(self, db_connection):
        self.db = db_connection
        self.students = db_connection.students
        self.courses = db_connection.courses
        self.instructors = db_connection.instructors
        self.enrollments = db_connection.enrollments

    # Complex Queries
    def find_students_by_major(self, major):
        """Find all students in a specific major"""
        return list(self.students.find({"major": major}))

    def find_students_by_year(self, year):
        """Find all students in a specific year (Freshman, Sophomore, etc.)"""
        return list(self.students.find({"year": year}))

    def find_courses_by_instructor(self, instructor_id):
        """Find all courses taught by a specific instructor"""
        return list(self.courses.find({"instructor_id": instructor_id}))

    def find_enrollments_by_status(self, status):
        """Find all enrollments with a specific status"""
        return list(self.enrollments.find({"status": status}))

    def find_students_with_gpa_above(self, gpa_threshold):
        """Find all students with GPA above a threshold"""
        return list(self.students.find({"gpa": {"$gte": gpa_threshold}}))

    def find_courses_by_credits(self, credits):
        """Find all courses with specific number of credits"""
        return list(self.courses.find({"credits": credits}))

    def find_students_in_course(self, course_code):
        """Find all students enrolled in a specific course"""
        enrollment_docs = list(self.enrollments.find({"course_code": course_code}))
        student_ids = [e["student_id"] for e in enrollment_docs]
        return list(self.students.find({"student_id": {"$in": student_ids}}))

    def find_courses_for_student(self, student_id):
        """Find all courses a student is enrolled in"""
        enrollment_docs = list(self.enrollments.find({"student_id": student_id}))
        course_codes = [e["course_code"] for e in enrollment_docs]
        return list(self.courses.find({"course_code": {"$in": course_codes}}))

    def find_students_by_semester_and_year(self, semester, year):
        """Find all students enrolled in courses during a specific semester and year"""
        course_docs = list(self.courses.find({"semester": semester, "year": year}))
        course_codes = [c["course_code"] for c in course_docs]
        enrollment_docs = list(self.enrollments.find({"course_code": {"$in": course_codes}}))
        student_ids = [e["student_id"] for e in enrollment_docs]
        return list(self.students.find({"student_id": {"$in": student_ids}}))

    # Aggregation Operations
    def get_average_gpa_by_major(self):
        """Calculate average GPA grouped by major"""
        pipeline = [
            {
                "$group": {
                    "_id": "$major",
                    "average_gpa": {"$avg": "$gpa"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"average_gpa": -1}
            }
        ]
        return list(self.students.aggregate(pipeline))

    # Advanced Filter Operations
    def filter_students(self, major=None, year=None, min_gpa=None, max_gpa=None):
        """Filter students by multiple criteria"""
        query = {}
        if major:
            query["major"] = major
        if year:
            query["year"] = year
        if min_gpa is not None or max_gpa is not None:
            gpa_query = {}
            try:
                if min_gpa is not None:
                    gpa_query["$gte"] = float(min_gpa)
                if max_gpa is not None:
                    gpa_query["$lte"] = float(max_gpa)
                query["gpa"] = gpa_query
            except (ValueError, TypeError):
                # Skip GPA filtering if invalid values provided
                pass
        
        return list(self.students.find(query))

    def filter_courses(self, instructor_id=None, credits=None, semester=None, year=None):
        """Filter courses by multiple criteria"""
        query = {}
        if instructor_id:
            query["instructor_id"] = instructor_id
        try:
            if credits:
                query["credits"] = int(credits)
            if year:
                query["year"] = int(year)
        except (ValueError, TypeError):
            # Skip numeric filtering if invalid values provided
            pass
        if semester:
            query["semester"] = semester
        
        return list(self.courses.find(query))

    def filter_instructors(self, department=None):
        """Filter instructors by department"""
        query = {}
        if department:
            query["department"] = department
        
        return list(self.instructors.find(query))

    def filter_enrollments(self, status=None, grade_min=None, grade_max=None, student_id=None, course_code=None):
        """Filter enrollments by multiple criteria"""
        query = {}
        if status:
            query["status"] = status
        if student_id:
            query["student_id"] = student_id
        if course_code:
            query["course_code"] = course_code
        
        # For grade filtering, we need to convert letter grades to numeric values
        if grade_min is not None or grade_max is not None:
            grade_mapping = {
                "A+": 4.0, "A": 4.0, "A-": 3.7,
                "B+": 3.3, "B": 3.0, "B-": 2.7,
                "C+": 2.3, "C": 2.0, "C-": 1.7,
                "D+": 1.3, "D": 1.0, "D-": 0.7,
                "F": 0.0
            }
            
            # This is a simplified approach - you might want to store numeric grades directly
            # or use more complex MongoDB queries for grade ranges
            pass  # Grade filtering would require additional implementation
        
        return list(self.enrollments.find(query))

    def get_available_majors(self):
        """Get all available majors"""
        return self.students.distinct("major")

    def get_available_years(self):
        """Get all available academic years"""
        return self.students.distinct("year")

    def get_available_departments(self):
        """Get all available departments"""
        return self.instructors.distinct("department")

    def get_available_semesters(self):
        """Get all available semesters"""
        return self.courses.distinct("semester")

    def get_available_credits(self):
        """Get all available credit values"""
        return sorted(self.courses.distinct("credits"))

    def get_enrollment_count_by_course(self):
        """Get enrollment count for each course"""
        pipeline = [
            {
                "$group": {
                    "_id": "$course_code",
                    "enrollment_count": {"$sum": 1}
                }
            }
        ]
        return list(self.enrollments.aggregate(pipeline))

    def get_grade_distribution_for_course(self, course_code):
        """Get the distribution of grades for a specific course"""
        pipeline = [
            {
                "$match": {
                    "course_code": course_code,
                    "grade": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": "$grade",
                    "count": {"$sum": 1}
                }
            }
        ]
        return list(self.enrollments.aggregate(pipeline))

    def get_top_performing_students(self, limit=5):
        """Get the top N students by GPA"""
        return list(self.students.find().sort("gpa", DESCENDING).limit(limit))

    def get_courses_by_credits_and_semester(self, credits, semester):
        """Find courses with specific credits in a semester"""
        return list(self.courses.find({
            "credits": credits,
            "semester": semester
        }))

    def get_instructor_course_count(self):
        """Count number of courses taught by each instructor"""
        pipeline = [
            {
                "$group": {
                    "_id": "$instructor_id",
                    "course_count": {"$sum": 1}
                }
            }
        ]
        return list(self.courses.aggregate(pipeline))

    def get_passing_grade_enrollment_count(self):
        """Count enrollments with passing grades (C or higher)"""
        passing_grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C"]
        pipeline = [
            {
                "$match": {
                    "grade": {"$in": passing_grades}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "passing_enrollments": {"$sum": 1}
                }
            }
        ]
        return list(self.enrollments.aggregate(pipeline))

    def get_student_enrollment_history(self, student_id):
        """Get all courses a student has taken"""
        pipeline = [
            {
                "$match": {
                    "student_id": student_id
                }
            },
            {
                "$lookup": {
                    "from": "courses",
                    "localField": "course_code",
                    "foreignField": "course_code",
                    "as": "course_details"
                }
            }
        ]
        return list(self.enrollments.aggregate(pipeline))

    def get_average_credits_per_student_in_semester(self, semester, year):
        """Calculate average number of credits per student in a semester"""
        pipeline = [
            {
                "$match": {
                    "semester": semester,
                    "year": year
                }
            },
            {
                "$lookup": {
                    "from": "enrollments",
                    "localField": "course_code",
                    "foreignField": "course_code",
                    "as": "enrollments"
                }
            },
            {
                "$unwind": "$enrollments"
            },
            {
                "$group": {
                    "_id": "$enrollments.student_id",
                    "total_credits": {"$sum": "$credits"}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "average_credits": {"$avg": "$total_credits"}
                }
            }
        ]
        return list(self.courses.aggregate(pipeline))