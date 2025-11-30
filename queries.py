from pymongo import ASCENDING, DESCENDING
from datetime import datetime

class QueryOperations:
    def __init__(self, db_connection):
        self.db = db_connection
        self.students = db_connection.students
        self.courses = db_connection.courses
        self.instructors = db_connection.instructors
        self.enrollments = db_connection.enrollments

    # Queries
    def find_students_by_major(self, major):
        """Students by major"""
        return list(self.students.find({"major": major}))

    def find_students_by_year(self, year):
        """Students by year"""
        return list(self.students.find({"year": year}))

    def find_courses_by_instructor(self, instructor_id):
        """Courses by instructor"""
        return list(self.courses.find({"instructor_id": instructor_id}))

    def find_enrollments_by_status(self, status):
        """Enrollments by status"""
        return list(self.enrollments.find({"status": status}))

    def find_students_with_gpa_above(self, gpa_threshold):
        """Students above GPA"""
        return list(self.students.find({"gpa": {"$gte": gpa_threshold}}))

    def find_courses_by_credits(self, credits):
        """Courses by credits"""
        return list(self.courses.find({"credits": credits}))

    def find_students_in_course(self, course_code):
        """Students in course"""
        enrollment_docs = list(self.enrollments.find({"course_code": course_code}))
        student_ids = [e["student_id"] for e in enrollment_docs]
        return list(self.students.find({"student_id": {"$in": student_ids}}))

    def find_courses_for_student(self, student_id):
        """Courses for student"""
        enrollment_docs = list(self.enrollments.find({"student_id": student_id}))
        course_codes = [e["course_code"] for e in enrollment_docs]
        return list(self.courses.find({"course_code": {"$in": course_codes}}))

    def find_students_by_semester_and_year(self, semester, year):
        """Students by semester/year"""
        course_docs = list(self.courses.find({"semester": semester, "year": year}))
        course_codes = [c["course_code"] for c in course_docs]
        enrollment_docs = list(self.enrollments.find({"course_code": {"$in": course_codes}}))
        student_ids = [e["student_id"] for e in enrollment_docs]
        return list(self.students.find({"student_id": {"$in": student_ids}}))

    # Aggregations
    def get_average_gpa_by_major(self):
        """Avg GPA by major"""
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

    # Filters
    def filter_students(self, major=None, year=None, min_gpa=None, max_gpa=None):
        """Filter students"""
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
                # Skip invalid GPA
                pass
        
        return list(self.students.find(query))

    def filter_courses(self, instructor_id=None, credits=None, semester=None, year=None):
        """Filter courses"""
        query = {}
        if instructor_id:
            query["instructor_id"] = instructor_id
        try:
            if credits:
                query["credits"] = int(credits)
            if year:
                query["year"] = int(year)
        except (ValueError, TypeError):
            # Skip invalid numbers
            pass
        if semester:
            query["semester"] = semester
        
        return list(self.courses.find(query))

    def filter_instructors(self, department=None):
        """Filter instructors"""
        query = {}
        if department:
            query["department"] = department
        
        return list(self.instructors.find(query))

    def filter_enrollments(self, status=None, grade_min=None, grade_max=None, student_id=None, course_code=None):
        """Filter enrollments"""
        query = {}
        if status:
            query["status"] = status
        if student_id:
            query["student_id"] = student_id
        if course_code:
            query["course_code"] = course_code
        
        # Convert grades to numbers
        if grade_min is not None or grade_max is not None:
            grade_mapping = {
                "A+": 4.0, "A": 4.0, "A-": 3.7,
                "B+": 3.3, "B": 3.0, "B-": 2.7,
                "C+": 2.3, "C": 2.0, "C-": 1.7,
                "D+": 1.3, "D": 1.0, "D-": 0.7,
                "F": 0.0
            }
            
            # Simplified grade approach
            pass  # Grade filtering would require additional implementation
        
        return list(self.enrollments.find(query))

    def get_available_majors(self):
        """Available majors"""
        return self.students.distinct("major")

    def get_available_years(self):
        """Available years"""
        return self.students.distinct("year")

    def get_available_departments(self):
        """Available departments"""
        return self.instructors.distinct("department")

    def get_available_semesters(self):
        """Available semesters"""
        return self.courses.distinct("semester")

    def get_available_credits(self):
        """Available credits"""
        return sorted(self.courses.distinct("credits"))

    def get_enrollment_count_by_course(self):
        """Enrollment count by course"""
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
        """Grade distribution by course"""
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
        """Top students by GPA"""
        return list(self.students.find().sort("gpa", DESCENDING).limit(limit))

    def get_courses_by_credits_and_semester(self, credits, semester):
        """Courses by credits & semester"""
        return list(self.courses.find({
            "credits": credits,
            "semester": semester
        }))

    def get_instructor_course_count(self):
        """Course count per instructor"""
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
        """Passing grade enrollments"""
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
        """Student course history"""
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
        """Avg credits per student"""
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