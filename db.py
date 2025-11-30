from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

try:
    # Load environment variables from .env file if it exists
    load_dotenv()
    print("✅ Environment variables loaded")
except ImportError:
    print("⚠️  python-dotenv not installed, using default MongoDB settings")
except Exception as e:
    print(f"⚠️  Error loading .env file: {e}")

class Database:
    def __init__(self):
        # Get MongoDB URI from environment variable
        self.uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/student_course_db")
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Test the connection
            self.client.admin.command('ping')
            default_db = self.client.get_default_database()
            self.db = default_db if default_db is not None else self.client['student_course_db']
            
            # Collections
            self.students = self.db.students
            self.courses = self.db.courses
            self.instructors = self.db.instructors
            self.enrollments = self.db.enrollments
            print("✅ Connected to MongoDB successfully")
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {str(e)}")
            print("Please ensure MongoDB is running and accessible")
            raise

    def get_db(self):
        return self.db

    def close_connection(self):
        try:
            self.client.close()
            print("Database connection closed")
        except Exception:
            pass


class Student:
    def __init__(self, db_connection):
        self.collection = db_connection.students
        self.db = db_connection

    def create(self, student_data):
        """Insert a new student document"""
        try:
            student_data['created_at'] = datetime.now()
            student_data['updated_at'] = datetime.now()
            result = self.collection.insert_one(student_data)
            return result.inserted_id
        except Exception as e:
            if "duplicate key" in str(e).lower():
                raise ValueError(f"Student with ID '{student_data.get('student_id')}' already exists")
            elif "duplicate key" in str(e).lower() and "email" in str(e).lower():
                raise ValueError(f"Email '{student_data.get('email')}' is already in use")
            else:
                raise ValueError(f"Failed to create student: {str(e)}")

    def find_by_id(self, student_id):
        """Find a student by student_id"""
        return self.collection.find_one({"student_id": student_id})

    def find_all(self):
        """Find all students"""
        return list(self.collection.find())

    def update(self, student_id, update_data):
        """Update a student document"""
        update_data['updated_at'] = datetime.now()
        result = self.collection.update_one(
            {"student_id": student_id}, 
            {"$set": update_data}
        )
        return result.modified_count

    def delete(self, student_id):
        """Delete a student document and related enrollments"""
        # First delete all enrollments for this student
        self.db.enrollments.delete_many({"student_id": student_id})
        # Then delete the student
        result = self.collection.delete_one({"student_id": student_id})
        return result.deleted_count


class Course:
    def __init__(self, db_connection):
        self.collection = db_connection.courses
        self.db = db_connection

    def create(self, course_data):
        """Insert a new course document"""
        course_data['created_at'] = datetime.now()
        course_data['updated_at'] = datetime.now()
        result = self.collection.insert_one(course_data)
        return result.inserted_id

    def find_by_code(self, course_code):
        """Find a course by course_code"""
        return self.collection.find_one({"course_code": course_code})

    def find_all(self):
        """Find all courses"""
        return list(self.collection.find())

    def update(self, course_code, update_data):
        """Update a course document"""
        update_data['updated_at'] = datetime.now()
        result = self.collection.update_one(
            {"course_code": course_code}, 
            {"$set": update_data}
        )
        return result.modified_count

    def delete(self, course_code):
        """Delete a course document and related enrollments"""
        # First delete all enrollments for this course
        self.db.enrollments.delete_many({"course_code": course_code})
        # Then delete the course
        result = self.collection.delete_one({"course_code": course_code})
        return result.deleted_count


class Instructor:
    def __init__(self, db_connection):
        self.collection = db_connection.instructors
        self.db = db_connection

    def create(self, instructor_data):
        """Insert a new instructor document"""
        instructor_data['created_at'] = datetime.now()
        instructor_data['updated_at'] = datetime.now()
        result = self.collection.insert_one(instructor_data)
        return result.inserted_id

    def find_by_id(self, instructor_id):
        """Find an instructor by instructor_id"""
        return self.collection.find_one({"instructor_id": instructor_id})

    def find_all(self):
        """Find all instructors"""
        return list(self.collection.find())

    def update(self, instructor_id, update_data):
        """Update an instructor document"""
        update_data['updated_at'] = datetime.now()
        result = self.collection.update_one(
            {"instructor_id": instructor_id}, 
            {"$set": update_data}
        )
        return result.modified_count

    def delete(self, instructor_id):
        """Delete an instructor document and update related courses"""
        # Update all courses taught by this instructor to remove instructor assignment
        self.db.courses.update_many(
            {"instructor_id": instructor_id},
            {"$set": {"instructor_id": None}}
        )
        # Then delete the instructor
        result = self.collection.delete_one({"instructor_id": instructor_id})
        return result.deleted_count


class Enrollment:
    def __init__(self, db_connection):
        self.collection = db_connection.enrollments

    def create(self, enrollment_data):
        """Insert a new enrollment document"""
        enrollment_data['created_at'] = datetime.now()
        enrollment_data['updated_at'] = datetime.now()
        result = self.collection.insert_one(enrollment_data)
        return result.inserted_id

    def find_by_student_and_course(self, student_id, course_code):
        """Find an enrollment by student_id and course_code"""
        return self.collection.find_one({
            "student_id": student_id,
            "course_code": course_code
        })

    def find_by_student(self, student_id):
        """Find all enrollments for a student"""
        return list(self.collection.find({"student_id": student_id}))

    def find_by_course(self, course_code):
        """Find all enrollments for a course"""
        return list(self.collection.find({"course_code": course_code}))

    def update(self, student_id, course_code, update_data):
        """Update an enrollment document"""
        update_data['updated_at'] = datetime.now()
        result = self.collection.update_one(
            {"student_id": student_id, "course_code": course_code}, 
            {"$set": update_data}
        )
        return result.modified_count

    def delete(self, student_id, course_code):
        """Delete an enrollment document"""
        result = self.collection.delete_one({
            "student_id": student_id,
            "course_code": course_code
        })
        return result.deleted_count