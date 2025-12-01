#!/usr/bin/env python3
"""
Pretty print MongoDB collections for presentation
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import Database
from bson import json_util
import json
from tabulate import tabulate

def pretty_print_collection(collection_name, data):
    """Pretty print a collection with formatting"""
    print(f"\n{'='*60}")
    print(f"📋 COLLECTION: {collection_name.upper()}")
    print(f"{'='*60}")
    
    if not data:
        print("📭 No documents found")
        return
    
    print(f"📊 Total documents: {len(data)}")
    print("-" * 60)
    
    # Extract keys from first document for headers
    if data:
        keys = list(data[0].keys())
        
        # Prepare data for tabulate
        table_data = []
        for doc in data:
            row = []
            for key in keys:
                value = doc.get(key, "")
                # Handle nested objects and arrays
                if isinstance(value, dict):
                    if 'first' in value and 'last' in value:  # Name object
                        value = f"{value.get('first', '')} {value.get('last', '')}"
                    else:
                        value = json.dumps(value, default=str)
                elif isinstance(value, list):
                    value = ', '.join(map(str, value)) if value else "[]"
                row.append(str(value) if value is not None else "NULL")
            table_data.append(row)
        
        # Print table
        print(tabulate(table_data, headers=keys, tablefmt="grid", maxcolwidths=[20]*len(keys)))
        
        # Show sample document structure
        print(f"\n📄 Sample Document Structure:")
        print("-" * 40)
        sample_doc = json.dumps(data[0], indent=2, default=str)
        print(sample_doc)

def print_schema_summary():
    """Print database schema summary"""
    print("\n" + "="*80)
    print("🗄️  MONGODB DATABASE SCHEMA SUMMARY")
    print("="*80)
    
    schema = {
        "students": {
            "student_id": "String (Primary Key)",
            "name": {"first": "String", "last": "String"},
            "email": "String",
            "major": "String",
            "year": "String",
            "gpa": "Float",
            "created_at": "DateTime",
            "updated_at": "DateTime"
        },
        "courses": {
            "course_code": "String (Primary Key)",
            "title": "String",
            "description": "String",
            "credits": "Integer",
            "instructor_id": "String (Foreign Key)",
            "semester": "String",
            "year": "Integer",
            "prerequisites": "Array<String>",
            "created_at": "DateTime",
            "updated_at": "DateTime"
        },
        "instructors": {
            "instructor_id": "String (Primary Key)",
            "name": {"first": "String", "last": "String"},
            "email": "String",
            "department": "String",
            "created_at": "DateTime",
            "updated_at": "DateTime"
        },
        "enrollments": {
            "_id": "ObjectId",
            "student_id": "String (Foreign Key)",
            "course_code": "String (Foreign Key)",
            "status": "String (Active/Completed/Dropped/Withdrawn)",
            "created_at": "DateTime",
            "updated_at": "DateTime"
        }
    }
    
    for collection, fields in schema.items():
        print(f"\n📚 {collection.upper()}:")
        for field, type_info in fields.items():
            if isinstance(type_info, dict):
                print(f"  └── {field}: {type_info}")
            else:
                print(f"    ├── {field}: {type_info}")

def main():
    """Main function to display database"""
    print("🎓 MONGODB STUDENT COURSE DATABASE - PRETTY DISPLAY")
    print("="*60)
    
    try:
        # Connect to database
        db = Database()
        print("✅ Connected to MongoDB successfully!")
        
        # Print schema summary first
        print_schema_summary()
        
        # Collections to display
        collections = {
            "Students": db.students.find(),
            "Courses": db.courses.find(), 
            "Instructors": db.instructors.find(),
            "Enrollments": db.enrollments.find()
        }
        
        # Display each collection
        for name, cursor in collections.items():
            data = list(cursor)
            pretty_print_collection(name, data)
        
        # Print relationships
        print("\n" + "="*80)
        print("🔗 DATABASE RELATIONSHIPS")
        print("="*80)
        print("📊 students (1) ←→ (many) enrollments (many) ←→ (1) courses")
        print("👨‍🏫 instructors (1) ←→ (many) courses")
        print("📚 courses (many) ←→ (many) prerequisites (self-reference)")
        
        # Close connection
        db.close_connection()
        print("\n✅ Database display completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
