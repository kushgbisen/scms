#!/usr/bin/env python3
"""
Migrate data from local MongoDB to Atlas Atlas
"""

import os
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import string

def generate_realistic_id(prefix, length=6):
    """Generate realistic ID with prefix"""
    return f"{prefix}{random.randint(10**(length-1), 10**length-1)}"

def generate_realistic_name():
    """Generate realistic name"""
    first_names = [
        "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason", 
        "Isabella", "William", "Mia", "James", "Charlotte", "Benjamin", 
        "Amelia", "Lucas", "Harper", "Henry", "Evelyn", "Alexander"
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
        "Davis", "Rodriguez", "Martinez", "Anderson", "Taylor", "Thomas", 
        "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris"
    ]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_realistic_email(name, domain="edu"):
    """Generate realistic email"""
    first, last = name.lower().replace(" ", "-").split("-")
    numbers = random.randint(1, 99)
    
    if domain == "edu":
        universities = ["university.edu", "college.edu", "tech.edu", "state.edu", "inst.edu"]
        return f"{first}.{last}{numbers}@{random.choice(universities)}"
    else:
        domains = ["gmail.com", "outlook.com", "yahoo.com", "protonmail.com"]
        return f"{first}.{last}{numbers}@{random.choice(domains)}"

def main():
    print("🚀 Migrating to MongoDB Atlas")
    print("=" * 40)
    
    try:
        # Connect to Atlas
        atlas_uri = "mongodb+srv://kushgbisen:password1234@clusterscms.2uq6oeu.mongodb.net/student_course_db?retryWrites=true&w=majority"
        print("✅ Connecting to Atlas...")
        atlas_client = MongoClient(atlas_uri, serverSelectionTimeoutMS=10000)
        atlas_client.admin.command('ping')
        atlas_db = atlas_client.student_course_db
        
        print("✅ Connected to MongoDB Atlas")
        
        # Clear existing data in Atlas
        print("🗑️  Clearing existing Atlas data...")
        atlas_db.students.delete_many({})
        atlas_db.courses.delete_many({})
        atlas_db.instructors.delete_many({})
        atlas_db.enrollments.delete_many({})
        
        # Majors and courses data
        majors = {
            "Computer Science": ["CS", 15],
            "Data Science": ["DS", 12], 
            "Mathematics": ["MATH", 8],
            "Biology": ["SCI", 6],
            "Chemistry": ["SCI", 4],
            "Physics": ["SCI", 3],
            "Business": ["BUS", 9],
            "Engineering": ["ENG", 11]
        }
        
        courses_data = {
            "Computer Science": [
                "Introduction to Programming", "Data Structures & Algorithms", 
                "Computer Networks", "Database Systems", "Operating Systems"
            ],
            "Mathematics": [
                "Calculus I", "Calculus II", "Linear Algebra", "Differential Equations",
                "Probability & Statistics"
            ],
            "Biology": [
                "Cell Biology", "Molecular Biology", "Genetics", "Evolution",
                "Ecology"
            ],
            "Chemistry": [
                "General Chemistry", "Organic Chemistry", "Physical Chemistry",
                "Analytical Chemistry", "Biochemistry"
            ],
            "Physics": [
                "Classical Mechanics", "Electromagnetism", "Quantum Mechanics",
                "Thermodynamics", "Optics"
            ]
        }
        
        # Generate Instructors
        print("👥 Generating instructors...")
        instructors = []
        
        for i, major in enumerate(majors.keys()):
            instructor_name = generate_realistic_name()
            first, last = instructor_name.split(" ", 1)
            
            instructor = {
                "instructor_id": f"INS{i+1:03d}",
                "name": {"first": first, "last": last},
                "email": generate_realistic_email(instructor_name, "prof"),
                "department": major,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            instructors.append(instructor)
        
        # Insert instructors in batch
        if instructors:
            atlas_db.instructors.insert_many(instructors)
            print(f"✅ Inserted {len(instructors)} instructors")
        
        # Generate Courses
        print("📚 Generating courses...")
        courses = []
        course_code_counter = 1
        
        for major, course_list in courses_data.items():
            for course_name in course_list:
                # Find appropriate instructor
                dept_instructors = [ins for ins in instructors if ins["department"] == major]
                instructor = dept_instructors[0] if dept_instructors else instructors[0]
                
                course = {
                    "course_code": f"{majors[major][0]}{100 + course_code_counter}",
                    "title": course_name,
                    "description": f"Comprehensive study of {course_name.lower()}",
                    "credits": random.choice([3, 4]),
                    "instructor_id": instructor["instructor_id"],
                    "semester": random.choice(["Fall", "Spring"]),
                    "year": 2024,
                    "prerequisites": [],
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
                
                courses.append(course)
                course_code_counter += 1
        
        # Insert courses in batch
        if courses:
            atlas_db.courses.insert_many(courses)
            print(f"✅ Inserted {len(courses)} courses")
        
        # Generate Students
        print("👨‍🎓 Generating students...")
        students = []
        
        for major_info, (prefix, num_students) in majors.items():
            for i in range(num_students):
                student_name = generate_realistic_name()
                first, last = student_name.split(" ", 1)
                
                student = {
                    "student_id": f"{prefix}{10000 + i}",
                    "name": {"first": first, "last": last},
                    "email": generate_realistic_email(student_name, "edu"),
                    "major": major_info,
                    "year": random.choice(["Freshman", "Sophomore", "Junior", "Senior"]),
                    "gpa": round(random.uniform(2.5, 4.0), 2),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
                
                students.append(student)
        
        # Insert students in batch
        if students:
            atlas_db.students.insert_many(students)
            print(f"✅ Inserted {len(students)} students")
        
        # Generate Enrollments
        print("📝 Generating enrollments...")
        enrollments = []
        
        for student in students:
            # Enroll each student in 3-5 courses
            student_courses = random.sample(courses, random.randint(3, 5))
            
            for course in student_courses:
                enrollment = {
                    "student_id": student["student_id"],
                    "course_code": course["course_code"],
                    "status": random.choice(["Active", "Completed", "Dropped"]),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
                
                enrollments.append(enrollment)
        
        # Insert enrollments in batch
        if enrollments:
            atlas_db.enrollments.insert_many(enrollments)
            print(f"✅ Inserted {len(enrollments)} enrollments")
        
        # Print statistics
        print("\n📊 Atlas Database Statistics:")
        print(f"   Students: {atlas_db.students.count_documents({})}")
        print(f"   Courses: {atlas_db.courses.count_documents({})}")  
        print(f"   Instructors: {atlas_db.instructors.count_documents({})}")
        print(f"   Enrollments: {atlas_db.enrollments.count_documents({})}")
        
        print("\n🎯 Migration to Atlas completed successfully!")
        print("Your Vercel app should now show data!")
        
        # Close connection
        atlas_client.close()
        
    except Exception as e:
        print(f"❌ Error during migration: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
