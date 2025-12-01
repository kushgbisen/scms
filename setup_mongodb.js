// MongoDB Database Setup Script
// Execute with: mongosh "mongodb://localhost:27017/student_course_db" setup_mongodb.js

// Create and use database
db = db.getSiblingDB('student_course_db');

print("Starting MongoDB database setup...");

// Clear existing data
print("Clearing existing data...");
db.students.deleteMany({});
db.courses.deleteMany({});
db.instructors.deleteMany({});
db.enrollments.deleteMany({});

// Insert Instructors
print("Inserting instructors...");
db.instructors.insertMany([
  {
    instructor_id: "INS001",
    name: { first: "John", last: "Anderson" },
    email: "john.anderson@university.edu",
    department: "Computer Science",
    title: "Professor",
    specialization: "Machine Learning",
    hire_date: "2015-08-15",
    office: "Building A-101",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    instructor_id: "INS002",
    name: { first: "Sarah", last: "Mitchell" },
    email: "sarah.mitchell@university.edu",
    department: "Mathematics",
    title: "Associate Professor",
    specialization: "Linear Algebra",
    hire_date: "2018-08-20",
    office: "Building B-205",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    instructor_id: "INS003",
    name: { first: "Michael", last: "Chen" },
    email: "michael.chen@university.edu",
    department: "Biology",
    title: "Professor",
    specialization: "Genetics",
    hire_date: "2012-09-01",
    office: "Building C-150",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    instructor_id: "INS004",
    name: { first: "Emily", last: "Roberts" },
    email: "emily.roberts@university.edu",
    department: "Business",
    title: "Assistant Professor",
    specialization: "Finance",
    hire_date: "2020-08-10",
    office: "Building D-300",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    instructor_id: "INS005",
    name: { first: "David", last: "Thompson" },
    email: "david.thompson@university.edu",
    department: "Physics",
    title: "Lecturer",
    specialization: "Quantum Mechanics",
    hire_date: "2021-08-15",
    office: "Building E-250",
    created_at: new Date(),
    updated_at: new Date()
  }
]);

// Insert Courses
print("Inserting courses...");
db.courses.insertMany([
  {
    course_code: "CS101",
    title: "Introduction to Programming",
    description: "Fundamental concepts of programming using Python.",
    credits: 3,
    instructor_id: "INS001",
    instructor_name: "John Anderson",
    department: "Computer Science",
    semester: "Fall",
    year: 2024,
    level: 100,
    capacity: 50,
    prerequisites: [],
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    course_code: "CS201",
    title: "Data Structures & Algorithms",
    description: "Advanced data structures and algorithm analysis.",
    credits: 4,
    instructor_id: "INS001",
    instructor_name: "John Anderson",
    department: "Computer Science",
    semester: "Fall",
    year: 2024,
    level: 200,
    capacity: 40,
    prerequisites: ["CS101"],
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    course_code: "CS301",
    title: "Machine Learning",
    description: "Introduction to machine learning algorithms and applications.",
    credits: 4,
    instructor_id: "INS001",
    instructor_name: "John Anderson",
    department: "Computer Science",
    semester: "Spring",
    year: 2024,
    level: 300,
    capacity: 30,
    prerequisites: ["CS201", "MATH201"],
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    course_code: "MATH101",
    title: "Calculus I",
    description: "Differential and integral calculus.",
    credits: 4,
    instructor_id: "INS002",
    instructor_name: "Sarah Mitchell",
    department: "Mathematics",
    semester: "Fall",
    year: 2024,
    level: 100,
    capacity: 60,
    prerequisites: [],
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    course_code: "MATH201",
    title: "Linear Algebra",
    description: "Vector spaces, matrices, and linear transformations.",
    credits: 3,
    instructor_id: "INS002",
    instructor_name: "Sarah Mitchell",
    department: "Mathematics",
    semester: "Spring",
    year: 2024,
    level: 200,
    capacity: 35,
    prerequisites: ["MATH101"],
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    course_code: "BIO101",
    title: "Cell Biology",
    description: "Structure and function of cells.",
    credits: 3,
    instructor_id: "INS003",
    instructor_name: "Michael Chen",
    department: "Biology",
    semester: "Fall",
    year: 2024,
    level: 100,
    capacity: 45,
    prerequisites: [],
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    course_code: "BUS101",
    title: "Introduction to Business",
    description: "Fundamental business concepts and practices.",
    credits: 3,
    instructor_id: "INS004",
    instructor_name: "Emily Roberts",
    department: "Business",
    semester: "Fall",
    year: 2024,
    level: 100,
    capacity: 80,
    prerequisites: [],
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    course_code: "PHYS201",
    title: "Classical Mechanics",
    description: "Newtonian mechanics and applications.",
    credits: 4,
    instructor_id: "INS005",
    instructor_name: "David Thompson",
    department: "Physics",
    semester: "Fall",
    year: 2024,
    level: 200,
    capacity: 25,
    prerequisites: ["MATH101"],
    created_at: new Date(),
    updated_at: new Date()
  }
]);

// Insert Students
print("Inserting students...");
db.students.insertMany([
  {
    student_id: "CS10001",
    name: { first: "Emma", last: "Wilson" },
    email: "emma.wilson23@university.edu",
    major: "Computer Science",
    year: "Junior",
    gpa: 3.8,
    credits_completed: 75,
    enrollment_date: "2022-09-01",
    status: "Active",
    advisor_id: "INS001",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    student_id: "CS10002",
    name: { first: "Liam", last: "Johnson" },
    email: "liam.johnson45@university.edu",
    major: "Computer Science",
    year: "Sophomore",
    gpa: 3.5,
    credits_completed: 45,
    enrollment_date: "2023-09-01",
    status: "Active",
    advisor_id: "INS001",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    student_id: "MATH10001",
    name: { first: "Olivia", last: "Martinez" },
    email: "olivia.martinez67@university.edu",
    major: "Mathematics",
    year: "Senior",
    gpa: 3.9,
    credits_completed: 110,
    enrollment_date: "2021-09-01",
    status: "Active",
    advisor_id: "INS002",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    student_id: "BIO10001",
    name: { first: "Noah", last: "Davis" },
    email: "noah.davis89@university.edu",
    major: "Biology",
    year: "Junior",
    gpa: 3.6,
    credits_completed: 80,
    enrollment_date: "2022-09-01",
    status: "Active",
    advisor_id: "INS003",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    student_id: "BUS10001",
    name: { first: "Ava", last: "Brown" },
    email: "ava.brown12@university.edu",
    major: "Business",
    year: "Freshman",
    gpa: 3.2,
    credits_completed: 15,
    enrollment_date: "2023-09-01",
    status: "Active",
    advisor_id: "INS004",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    student_id: "PHYS10001",
    name: { first: "Ethan", last: "Miller" },
    email: "ethan.miller34@university.edu",
    major: "Physics",
    year: "Sophomore",
    gpa: 3.4,
    credits_completed: 40,
    enrollment_date: "2022-09-01",
    status: "Active",
    advisor_id: "INS005",
    created_at: new Date(),
    updated_at: new Date()
  }
]);

// Insert Enrollments
print("Inserting enrollments...");
db.enrollments.insertMany([
  // Emma Wilson - CS Major
  { student_id: "CS10001", course_code: "CS101", status: "completed", enrollment_date: "2022-09-01", grade: "A", completion_date: "2022-12-15", created_at: new Date(), updated_at: new Date() },
  { student_id: "CS10001", course_code: "CS201", status: "completed", enrollment_date: "2023-09-01", grade: "A-", completion_date: "2023-12-15", created_at: new Date(), updated_at: new Date() },
  { student_id: "CS10001", course_code: "CS301", status: "enrolled", enrollment_date: "2024-09-01", grade: null, created_at: new Date(), updated_at: new Date() },
  { student_id: "CS10001", course_code: "MATH101", status: "completed", enrollment_date: "2022-09-01", grade: "B+", completion_date: "2022-12-15", created_at: new Date(), updated_at: new Date() },
  
  // Liam Johnson - CS Major
  { student_id: "CS10002", course_code: "CS101", status: "completed", enrollment_date: "2023-09-01", grade: "B+", completion_date: "2023-12-15", created_at: new Date(), updated_at: new Date() },
  { student_id: "CS10002", course_code: "MATH101", status: "enrolled", enrollment_date: "2024-09-01", grade: null, created_at: new Date(), updated_at: new Date() },
  
  // Olivia Martinez - Math Major
  { student_id: "MATH10001", course_code: "MATH101", status: "completed", enrollment_date: "2021-09-01", grade: "A", completion_date: "2021-12-15", created_at: new Date(), updated_at: new Date() },
  { student_id: "MATH10001", course_code: "MATH201", status: "completed", enrollment_date: "2022-09-01", grade: "A", completion_date: "2022-12-15", created_at: new Date(), updated_at: new Date() },
  { student_id: "MATH10001", course_code: "PHYS201", status: "completed", enrollment_date: "2023-09-01", grade: "B", completion_date: "2023-12-15", created_at: new Date(), updated_at: new Date() },
  
  // Noah Davis - Biology Major
  { student_id: "BIO10001", course_code: "BIO101", status: "completed", enrollment_date: "2022-09-01", grade: "A-", completion_date: "2022-12-15", created_at: new Date(), updated_at: new Date() },
  { student_id: "BIO10001", course_code: "MATH101", status: "completed", enrollment_date: "2022-09-01", grade: "B+", completion_date: "2022-12-15", created_at: new Date(), updated_at: new Date() },
  { student_id: "BIO10001", course_code: "CS101", status: "enrolled", enrollment_date: "2024-09-01", grade: null, created_at: new Date(), updated_at: new Date() },
  
  // Ava Brown - Business Major
  { student_id: "BUS10001", course_code: "BUS101", status: "enrolled", enrollment_date: "2024-09-01", grade: null, created_at: new Date(), updated_at: new Date() },
  { student_id: "BUS10001", course_code: "MATH101", status: "enrolled", enrollment_date: "2024-09-01", grade: null, created_at: new Date(), updated_at: new Date() },
  
  // Ethan Miller - Physics Major
  { student_id: "PHYS10001", course_code: "MATH101", status: "completed", enrollment_date: "2022-09-01", grade: "B", completion_date: "2022-12-15", created_at: new Date(), updated_at: new Date() },
  { student_id: "PHYS10001", course_code: "PHYS201", status: "enrolled", enrollment_date: "2024-09-01", grade: null, created_at: new Date(), updated_at: new Date() }
]);

// Verify data population
print("\n=== DATABASE STATISTICS ===");
print("Students: " + db.students.countDocuments());
print("Courses: " + db.courses.countDocuments());
print("Instructors: " + db.instructors.countDocuments());
print("Enrollments: " + db.enrollments.countDocuments());

print("\n=== DEMONSTRATION QUERIES ===");
print("\nComputer Science students:");
db.students.find({ major: "Computer Science" }).forEach(printjson);

print("\nCourses taught by INS001:");
db.courses.find({ instructor_id: "INS001" }).forEach(printjson);

print("\nEnrollments for CS10001:");
db.enrollments.find({ student_id: "CS10001" }).forEach(printjson);

print("\nAverage GPA by major:");
db.students.aggregate([
  { $group: { _id: "$major", avgGpa: { $avg: "$gpa" }, count: { $sum: 1 } } },
  { $sort: { avgGpa: -1 } }
]).forEach(printjson);

print("\nDatabase setup completed successfully!");
