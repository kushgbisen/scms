# Student Course Management System - ER Diagram & Schema

## Entity Relationship Diagram

```mermaid
erDiagram
    STUDENTS ||--o{ ENROLLMENTS : enrolls_in
    COURSES ||--o{ ENROLLMENTS : has_enrollments
    INSTRUCTORS ||--o{ COURSES : teaches
    STUDENTS }o--|| INSTRUCTORS : advised_by
    
    STUDENTS {
        string student_id PK
        object name { first, last }
        string email
        string major
        string year
        float gpa
        int credits_completed
        string status
        string advisor_id FK
        date enrollment_date
        datetime created_at
        datetime updated_at
    }
    
    COURSES {
        string course_code PK
        string title
        string description
        int credits
        string instructor_id FK
        string instructor_name
        string department
        string semester
        int year
        int level
        int capacity
        array prerequisites
        datetime created_at
        datetime updated_at
    }
    
    INSTRUCTORS {
        string instructor_id PK
        object name { first, last }
        string email
        string department
        string title
        string specialization
        date hire_date
        string office
        datetime created_at
        datetime updated_at
    }
    
    ENROLLMENTS {
        string student_id FK
        string course_code FK
        string status
        string grade
        date enrollment_date
        date completion_date
        datetime created_at
        datetime updated_at
    }
```

## Detailed Collection Schemas

### Students Collection
```json
{
  "_id": ObjectId("..."),
  "student_id": "CS100123", // Unique alphanumeric identifier
  "name": {
    "first": "John",
    "last": "Doe"
  },
  "email": "john.doe@university.edu", // RFC-5322 compliant
  "major": "Computer Science",
  "year": "Junior", // Freshman|Sophomore|Junior|Senior
  "gpa": 3.75, // Range: 0.0-4.0
  "credits_completed": 45, // Range: 0-150
  "status": "Active", // Active|On Leave
  "advisor_id": "INS001", // FK to instructors
  "enrollment_date": ISODate("2022-09-01"),
  "created_at": ISODate("2024-01-01T00:00:00Z"),
  "updated_at": ISODate("2024-01-01T00:00:00Z")
}
```

### Courses Collection
```json
{
  "_id": ObjectId("..."),
  "course_code": "CS301", // Unique identifier
  "title": "Data Structures & Algorithms",
  "description": "Comprehensive study of data structures",
  "credits": 4, // Range: 1-6
  "instructor_id": "INS001", // FK to instructors
  "instructor_name": "Dr. Jane Smith", // Denormalized for quick access
  "department": "Computer Science",
  "semester": "Fall", // Fall|Spring|Summer
  "year": 2024, // Four-digit year
  "level": 300, // 100|200|300|400
  "capacity": 150, // Range: 10-200
  "prerequisites": ["CS101", "CS201"], // Array of course codes
  "created_at": ISODate("2024-01-01T00:00:00Z"),
  "updated_at": ISODate("2024-01-01T00:00:00Z")
}
```

### Instructors Collection
```json
{
  "_id": ObjectId("..."),
  "instructor_id": "INS001", // Unique identifier
  "name": {
    "first": "Jane",
    "last": "Smith"
  },
  "email": "jane.smith@university.edu",
  "department": "Computer Science",
  "title": "Assistant Professor", // Professor|Associate Professor|Assistant Professor|Lecturer
  "specialization": "Machine Learning",
  "hire_date": ISODate("2020-01-15"),
  "office": "Building A, Room 101",
  "created_at": ISODate("2024-01-01T00:00:00Z"),
  "updated_at": ISODate("2024-01-01T00:00:00Z")
}
```

### Enrollments Collection (Relationship/Junction)
```json
{
  "_id": ObjectId("..."),
  "student_id": "CS100123", // Composite key part 1
  "course_code": "CS301", // Composite key part 2
  "status": "Active", // Active|Completed|Dropped|Withdrawn
  "grade": "A-", // A+|A|A-|B+|B|B-|C+|C|C-|D+|D|D-|F
  "enrollment_date": ISODate("2024-08-15"),
  "completion_date": null, // Null if not completed
  "created_at": ISODate("2024-08-15T10:30:00Z"),
  "updated_at": ISODate("2024-08-15T10:30:00Z")
}
```

## Indexes and Performance Optimization

### Primary Indexes
```javascript
// Unique indexes for primary keys
db.students.createIndex({ "student_id": 1 }, { unique: true })
db.students.createIndex({ "email": 1 }, { unique: true })
db.courses.createIndex({ "course_code": 1 }, { unique: true })
db.instructors.createIndex({ "instructor_id": 1 }, { unique: true })

// Composite indexes for common queries
db.enrollments.createIndex({ student_id: 1, course_code: 1 }, { unique: true })
```

### Optimization Indexes
```javascript
// Student performance queries
db.students.createIndex({ "major": 1, "gpa": -1 })
db.students.createIndex({ "year": 1, "gpa": -1 })

// Course scheduling queries  
db.courses.createIndex({ "instructor_id": 1, "semester": 1, "year": 1 })
db.courses.createIndex({ "department": 1, "semester": 1, "year": 1 })

// Enrollment queries
db.enrollments.createIndex({ "course_code": 1, "status": 1 })
db.enrollments.createIndex({ "student_id": 1, "status": 1 })
```

### Text Search Indexes
```javascript
// Search functionality
db.students.createIndex({ 
  "name.first": "text", 
  "name.last": "text", 
  "major": "text" 
})

db.courses.createIndex({
  "title": "text",
  "description": "text",
  "department": "text"
})
```

## Data Relationships Summary

### Cardinality (Connection Count)
- **Students → Enrollments**: One-to-Many (1:N)
- **Courses → Enrollments**: One-to-Many (1:N) 
- **Students → Courses**: Many-to-Many (via Enrollments - Unordered)
- **Instructors → Courses**: One-to-Many (1:N)
- **Students → Advisor**: Many-to-One (N:1)

### Referential Integrity Actions
```python
# Student Deletion: Cascade delete enrollments
# Course Deletion: Cascade delete enrollments  
# Instructor Deletion: Remove from courses (set to null)
```

### Business Rules
1. **Unique Constraints**: Student ID, Email, Course Code, Instructor ID
2. **Grade Scale**: Letter grades with +/- system (A+ through F)
3. **Credit Range**: 1-6 credits per course
4. **GPA Range**: 0.0-4.0 scale
5. **Status Values**: Active, On Leave (Students); Active, Completed, Dropped, Withdrawn (Enrollments)

## Performance Characteristics
- **Entity Count**: 4 Collections (Students, Courses, Instructors, Enrollments)
- **Primary Relationships**: 4 Core Relationships
- **Index Count**: 12+ performance-optimized indexes
- **Composite Keys**: Multi-field indexes for complex queries
- **Query Patterns**: Aggregation pipelines, lookups, and advanced filtering
