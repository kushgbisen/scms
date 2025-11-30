# Student Course Management System

A modern MongoDB-based web application for managing student information, courses, enrollments, and academic records. Built with Flask and Bootstrap for a professional, responsive interface.

## 🌟 Features

**Core Management:**
- ✅ Student management (add, edit, delete, view)
- ✅ Course management with prerequisites
- ✅ Instructor management and scheduling
- ✅ Enrollment tracking and grade management
- ✅ Real-time data validation and error handling

**Advanced Features:**
- 📊 Interactive dashboard with analytics
- 🔍 Advanced search and filtering
- 📈 GPA analysis and performance insights
- 🗄️ Database optimization and indexing
- 📱 Responsive web interface

**Data Operations:**
- Complex MongoDB aggregation queries
- Cascade delete for data integrity
- Performance-optimized indexing
- Real-time statistics and reporting

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or Atlas)
- Modern web browser

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up MongoDB connection:**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB connection string
   ```

3. **Start the web application:**
   ```bash
   python run_web.py
   ```

4. **Open browser:**
   Navigate to http://localhost:5000

### Alternative: TUI Version
For command-line interface users:
```bash
python main.py
```

## 🖥️ Web Interface

The modern web interface provides:

- **Dashboard**: Overview with statistics and insights
- **Student Management**: Complete CRUD operations with validation
- **Course Management**: Prerequisites, scheduling, enrollment
- **Instructor Management**: Course assignments and department tracking
- **Analytics**: Advanced queries and performance metrics
- **Database Tools**: Indexing and maintenance

## 📊 Key Features

### Dashboard
- Real-time statistics
- Top performing students
- Average GPA by major
- Course enrollment metrics
- Quick action buttons

### Student Management
- Input validation (email, GPA ranges, required fields)
- Visual GPA indicators
- Academic status badges
- Enrollment tracking
- Performance analytics

### Advanced Queries
- Filter by major, GPA threshold, instructor
- Performance insights and recommendations
- Export capabilities
- Real-time search results

### Available Operations

The system provides the following functionality through its CLI:

1. **Student Management**:
   - Add, update, delete, and view students
   - List all students
   - Find students by major or GPA threshold

2. **Course Management**:
   - Add, update, delete, and view courses
   - List all courses

3. **Instructor Management**:
   - Add, update, delete, and view instructors
   - List all instructors

4. **Enrollment Management**:
   - Enroll students in courses
   - Drop students from courses
   - View student's enrollments
   - View course enrollments

5. **Advanced Queries**:
   - Find students by major
   - Find students with GPA above threshold
   - Find courses by instructor
   - Get average GPA by major
   - Get top performing students

6. **Performance Optimization**:
   - Create database indexes
   - List database indexes

## Project Structure

- `main.py` - Main application entry point with CLI
- `models.py` - Database models and connection, including CRUD operations
- `queries.py` - Complex queries and aggregation operations
- `indexing.py` - Database indexing for performance optimization
- `test.py` - Test suite to verify all functionality
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment file

## MongoDB Collections

The system uses four main collections:

1. **students**: Stores student information including ID, name, email, major, year, and GPA
2. **courses**: Contains course details like code, title, credits, instructor, and prerequisites
3. **instructors**: Holds instructor information including ID, name, email, and department
4. **enrollments**: Manages student enrollment in courses with status and grades

## MongoDB Features Demonstrated

This project implements several key MongoDB concepts from your course syllabus:

- **Document Data Model**: Complex nested documents with embedded objects
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Query Language**: Advanced querying with filters, projections, and conditions
- **Aggregation Pipeline**: Complex data analysis using MongoDB aggregation
- **Indexing**: Performance optimization with various index types
- **Relationships**: Reference-based relationships between collections

## Testing

Run the test suite to verify all functionality:
```bash
python test.py
```

The test suite verifies:
- Basic CRUD operations
- Complex queries and aggregations
- Indexing functionality
- Data integrity

## Development

To run the application in development mode:
1. Start your MongoDB instance
2. Set up the `.env` file with appropriate connection string
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python main.py`