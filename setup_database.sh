#!/bin/bash

# MongoDB Database Setup Script
# This script sets up the student course management database

echo "MongoDB Database Setup"
echo "======================"

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "Error: MongoDB is not running."
    echo "Please start MongoDB service first:"
    echo "  sudo systemctl start mongod"
    echo "  # or"
    echo "  mongod"
    exit 1
fi

# Check if mongosh is available
if ! command -v mongosh &> /dev/null; then
    echo "Error: mongosh is not available."
    echo "Please install MongoDB Shell (mongosh)."
    exit 1
fi

# MongoDB connection string
MONGODB_URI="mongodb://localhost:27017/student_course_db"

echo "Connecting to MongoDB..."
echo "URI: $MONGODB_URI"
echo ""

# Execute the setup script
if [ -f "setup_mongodb.js" ]; then
    echo "Running database setup script..."
    mongosh "$MONGODB_URI" setup_mongodb.js
    echo ""
    echo "Database setup completed!"
else
    echo "Error: setup_mongodb.js not found."
    exit 1
fi

echo ""
echo "To connect to your database manually:"
echo "  mongosh \"$MONGODB_URI\""
echo ""
echo "To run queries:"
echo "  mongosh \"$MONGODB_URI\" --eval \"db.students.find()\""
