#!/usr/bin/env python3
"""
Realistic data seeder for MongoDB database
"""

import random
import string
from datetime import datetime, timedelta
from db import Database, Student, Course, Instructor, Enrollment

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

def generate_course_code(subject, level, existing_codes):
    """Generate realistic unique course code"""
    subject_codes = {
        "CS": ["CS", "CSC", "CMP", "SE"],
        "MATH": ["MATH", "MAT", "CALC", "STAT"],
        "SCI": ["SCI", "BIO", "CHEM", "PHYS"],
        "ENG": ["ENG", "ENGL", "WRIT", "COMM"],
        "BUS": ["BUS", "MGT", "FIN", "ACCT"]
    }
    
    subject_prefix = random.choice(subject_codes[subject.split()[0]])
    
    # Try to generate a unique code
    attempts = 0
    while attempts < 10:
        course_num = f"{level}{random.randint(10, 99)}"
        course_code = f"{subject_prefix}{course_num}"
        if course_code not in existing_codes:
            return course_code
        attempts += 1
    
    # Fallback - just use a timestamp to make it unique
    course_code = f"{subject_prefix}{level}{random.randint(100, 999)}"
    return course_code

def main():
    print("🌱 Realistic MongoDB Data Seeder")
    print("=" * 40)
    
    try:
        db = Database()
        print("✅ Connected to MongoDB")
        
        # Clear existing data
        print("🗑️  Clearing existing data...")
        db.get_db().students.delete_many({})
        db.get_db().courses.delete_many({})
        db.get_db().instructors.delete_many({})
        db.get_db().enrollments.delete_many({})
        
        # Create models
        student_model = Student(db)
        course_model = Course(db)
        instructor_model = Instructor(db)
        enrollment_model = Enrollment(db)
        
        # Realistic majors and courses
        majors = {
            "Computer Science": ["CS", 150, 8.8],
            "Data Science": ["DS", 120, 7.2], 
            "Mathematics": ["MATH", 80, 4.5],
            "Biology": ["SCI", 60, 3.8],
            "Chemistry": ["SCI", 40, 2.9],
            "Physics": ["SCI", 30, 2.1],
            "Business": ["BUS", 90, 5.2],
            "Engineering": ["ENG", 110, 6.7]
        }
        
        # Realistic courses per major
        courses_data = {
            "Computer Science": [
                "Introduction to Programming", "Data Structures & Algorithms", 
                "Computer Networks", "Database Systems", "Operating Systems",
                "Software Engineering", "Machine Learning", "Artificial Intelligence",
                "Web Development", "Cybersecurity"
            ],
            "Mathematics": [
                "Calculus I", "Calculus II", "Linear Algebra", "Differential Equations",
                "Probability & Statistics", "Discrete Mathematics", "Number Theory",
                "Abstract Algebra", "Mathematical Analysis", "Complex Analysis"
            ],
            "Biology": [
                "Cell Biology", "Molecular Biology", "Genetics", "Evolution",
                "Ecology", "Biochemistry", "Microbiology", "Anatomy & Physiology",
                "Marine Biology", "Plant Biology"
            ],
            "Chemistry": [
                "General Chemistry", "Organic Chemistry", "Physical Chemistry",
                "Analytical Chemistry", "Biochemistry", "Inorganic Chemistry",
                "Environmental Chemistry", "Polymer Chemistry", "Medicinal Chemistry"
            ],
            "Physics": [
                "Classical Mechanics", "Electromagnetism", "Quantum Mechanics",
                "Thermodynamics", "Optics", "Nuclear Physics", "Astrophysics",
                "Particles & Fields", "Biophysics", "Condensed Matter Physics"
            ]
        }
        
        # Generate Instructors first
        print("👥 Generating realistic instructors...")
        instructors = []
        
        # Department heads and senior faculty
        for i, major in enumerate(majors.keys()):
            # Department head
            dept_head_name = generate_realistic_name()
            first, last = dept_head_name.split(" ", 1)
            
            instructor = {
                "instructor_id": f"INS{i+1:03d}",
                "name": {"first": first, "last": last},
                "email": generate_realistic_email(dept_head_name, "prof"),
                "department": major,
                "title": "Professor",
                "specialization": random.choice(courses_data.get(major, ["General"])),
                "hire_date": (datetime.now() - timedelta(days=random.randint(365, 3650))).strftime("%Y-%m-%d"),
                "office": f"Building {chr(65+i%8)}-{random.randint(100, 399)}"
            }
            instructors.append(instructor)
            instructor_model.create(instructor)
        
        # Additional faculty
        for i in range(10, 25):
            faculty_name = generate_realistic_name()
            first, last = faculty_name.split(" ", 1)
            major = random.choice(list(majors.keys()))
            
            instructor = {
                "instructor_id": f"INS{i:03d}",
                "name": {"first": first, "last": last},
                "email": generate_realistic_email(faculty_name, "prof"),
                "department": major,
                "title": random.choice(["Professor", "Associate Professor", "Assistant Professor", "Lecturer"]),
                "specialization": random.choice(courses_data.get(major, ["General"])),
                "hire_date": (datetime.now() - timedelta(days=random.randint(180, 1825))).strftime("%Y-%m-%d"),
                "office": f"Building {chr(65+i%8)}-{random.randint(100, 399)}"
            }
            instructors.append(instructor)
            instructor_model.create(instructor)
        
        print(f"✅ Created {len(instructors)} instructors")
        
        # Generate Courses
        print("📚 Generating realistic courses...")
        courses = []
        course_id = 0
        existing_course_codes = set()
        
        for major, course_list in courses_data.items():
            for course_name in course_list:
                course_id += 1
                
                # Find appropriate instructor
                dept_instructors = [ins for ins in instructors if ins["department"] == major]
                if not dept_instructors:
                    dept_instructors = instructors  # fallback to any instructor
                
                instructor = random.choice(dept_instructors)
                
                # Determine course level
                if course_name.startswith("Introduction") or "I" in course_name:
                    level = random.choice([100, 101, 102])
                elif course_name.startswith("Advanced") or "III" in course_name:
                    level = random.choice([300, 301, 302])
                else:
                    level = random.choice([200, 201, 202])
                
                course = {
                    "course_code": generate_course_code(majors[major][0], level, existing_course_codes),
                    "title": course_name,
                    "description": f"Comprehensive study of {course_name.lower()} with emphasis on fundamental concepts and practical applications.",
                    "credits": random.choice([3, 4]),
                    "instructor_id": instructor["instructor_id"],
                    "instructor_name": f"{instructor['name']['first']} {instructor['name']['last']}",
                    "department": major,
                    "semester": random.choice(["Fall", "Spring", "Summer"]),
                    "year": 2024,
                    "level": level,
                    "capacity": random.randint(25, 150),
                    "prerequisites": []
                }
                
                # Add some prerequisites for upper-level courses
                if level >= 200 and random.random() > 0.5:
                    # Find a lower-level course from same department as prerequisite
                    prereq_courses = [c["course_code"] for c in courses if c.get("department") == major and c.get("level", 0) < level]
                    if prereq_courses:
                        course["prerequisites"] = random.sample(prereq_courses, min(1, len(prereq_courses)))
                
                existing_course_codes.add(course["course_code"])
                courses.append(course)
                course_model.create(course)
        
        print(f"✅ Created {len(courses)} courses")
        
        # Generate Students
        print("👨‍🎓 Generating realistic students...")
        students = []
        existing_student_ids = set()
        existing_emails = set()
        
        for major_info, (prefix, num_students, avg_gpa_range) in majors.items():
            for i in range(num_students):
                # Generate unique student ID
                student_id = f"{prefix}{random.randint(10000, 99999)}"
                while student_id in existing_student_ids:
                    student_id = f"{prefix}{random.randint(10000, 99999)}"
                existing_student_ids.add(student_id)
                student_name = generate_realistic_name()
                first, last = student_name.split(" ", 1)
                
                # Generate unique email
                email = generate_realistic_email(student_name, "edu")
                while email in existing_emails:
                    # Add a number to make it unique
                    first, last = student_name.lower().replace(" ", "-").split("-")
                    email = f"{first}.{last}{random.randint(100, 999)}@{random.choice(['university.edu', 'college.edu', 'tech.edu'])}"
                existing_emails.add(email)
                
                # Realistic year distribution
                year_weights = [0.25, 0.3, 0.25, 0.2]  # Freshman, Sophomore, Junior, Senior
                year = random.choices(["Freshman", "Sophomore", "Junior", "Senior"], weights=year_weights)[0]
                
                # GPA tends to be lower for freshmen, higher for seniors
                if year == "Freshman":
                    gpa = round(random.uniform(2.8, 3.8), 2)
                elif year == "Senior":
                    gpa = round(random.uniform(3.2, 4.0), 2)
                else:
                    gpa = round(random.uniform(2.5, 3.9), 2)
                
                student = {
                    "student_id": student_id,
                    "name": {"first": first, "last": last},
                    "email": email,
                    "major": major_info,
                    "year": year,
                    "gpa": gpa,
                    "credits_completed": random.randint(0, 120),
                    "enrollment_date": (datetime.now() - timedelta(days=random.randint(30, 1460))).strftime("%Y-%m-%d"),
                    "status": random.choice(["Active", "Active", "Active", "On Leave"]),  # Most students are active
                    "advisor_id": random.choice([ins["instructor_id"] for ins in instructors if ins["department"] == major_info])
                }
                
                students.append(student)
                student_model.create(student)
        
        print(f"✅ Created {len(students)} students")
        
        # Generate Realistic Enrollments
        print("📝 Generating realistic enrollments...")
        enrollments = []
        
        for student in students:
            # Determine number of courses based on student year
            if student["year"] == "Freshman":
                num_courses = random.randint(3, 5)
            elif student["year"] == "Senior":
                num_courses = random.randint(4, 6)
            else:
                num_courses = random.randint(4, 5)
            
            # Get available courses for student's major
            major_courses = [c for c in courses if c["department"] == student["major"]]
            if not major_courses:
                major_courses = courses  # fallback
            
            # Select courses (simplified for now)
            available_courses = random.sample(major_courses, min(num_courses * 2, len(major_courses)))
            selected_courses = available_courses[:num_courses]
            
            for course in selected_courses:
                # Realistic enrollment status based on course level and student year
                if course.get("level", 200) > 300 and student["year"] in ["Freshman", "Sophomore"]:
                    status = random.choice(["enrolled", "dropped", "enrolled"])
                elif random.random() > 0.2:  # 80% complete their courses
                    status = "completed"
                else:
                    status = random.choice(["enrolled", "dropped"])
                
                enrollment = {
                    "student_id": student["student_id"],
                    "course_code": course["course_code"],
                    "status": status,
                    "enrollment_date": (datetime.now() - timedelta(days=random.randint(1, 120))).strftime("%Y-%m-%d"),
                    "grade": None
                }
                
                # Add grade for completed courses
                if status == "completed":
                    if student["gpa"] >= 3.7:
                        grade = random.choices(["A", "A-", "B+"], weights=[0.6, 0.3, 0.1])[0]
                    elif student["gpa"] >= 3.3:
                        grade = random.choices(["B+", "B", "B-", "A-"], weights=[0.3, 0.4, 0.2, 0.1])[0]
                    elif student["gpa"] >= 2.7:
                        grade = random.choices(["B", "B-", "C+", "C"], weights=[0.3, 0.3, 0.2, 0.2])[0]
                    else:
                        grade = random.choices(["C", "C-", "D", "D+"], weights=[0.4, 0.3, 0.2, 0.1])[0]
                    
                    enrollment["grade"] = grade
                    enrollment["completion_date"] = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
                
                enrollments.append(enrollment)
                enrollment_model.create(enrollment)
        
        print(f"✅ Created {len(enrollments)} enrollments")
        
        # Print statistics
        print("\n📊 Database Statistics:")
        print(f"   Students: {len(students)}")
        print(f"   Courses: {len(courses)}")  
        print(f"   Instructors: {len(instructors)}")
        print(f"   Enrollments: {len(enrollments)}")
        
        # Show major distribution
        print("\n🎓 Students by Major:")
        for major in majors.keys():
            count = sum(1 for s in students if s["major"] == major)
            avg_gpa = sum(s["gpa"] for s in students if s["major"] == major) / count if count > 0 else 0
            print(f"   {major}: {count} students (Avg GPA: {avg_gpa:.2f})")
        
        print("\n🎯 Data seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
