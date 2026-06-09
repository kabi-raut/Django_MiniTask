import csv
import os
from pathlib import Path


class StudentRecordError(Exception):
    """Custom exception for student record operations"""
    pass


class Student:
    """Student class with encapsulation"""
    def __init__(self, roll_no, name, email, marks):
        self.roll_no = roll_no
        self.name = name
        self.email = email
        self.marks = marks

    def __str__(self):
        return f"Roll: {self.roll_no}, Name: {self.name}, Email: {self.email}, Marks: {self.marks}"

    def to_dict(self):
        return {
            'roll_no': self.roll_no,
            'name': self.name,
            'email': self.email,
            'marks': self.marks
        }


class StudentRecordManager:
    """Manages student records with file handling"""

    def __init__(self, csv_file=None):
        if csv_file is None:
            base_dir = Path(__file__).resolve().parent
            csv_file = base_dir / 'students.csv'
        self.csv_file = csv_file
        self._initialize_csv()

    def _initialize_csv(self):
        """Create CSV file if it doesn't exist"""
        if not os.path.exists(self.csv_file):
            try:
                with open(self.csv_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['roll_no', 'name', 'email', 'marks'])
            except IOError as e:
                raise StudentRecordError(f"Could not create CSV file: {e}")

    def add_student(self, student):
        """Add a student record"""
        try:
            if not isinstance(student, Student):
                raise StudentRecordError("Invalid student object")

            # Check if roll number already exists
            if self._roll_no_exists(student.roll_no):
                raise StudentRecordError(f"Roll number {student.roll_no} already exists")

            with open(self.csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([student.roll_no, student.name, student.email, student.marks])
        except (IOError, StudentRecordError) as e:
            raise StudentRecordError(f"Error adding student: {e}")

    def _roll_no_exists(self, roll_no):
        """Check if roll number exists"""
        try:
            with open(self.csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row and row['roll_no'] == str(roll_no):
                        return True
            return False
        except IOError as e:
            raise StudentRecordError(f"Error reading CSV: {e}")

    def get_all_students(self):
        """Get all students"""
        try:
            students = []
            with open(self.csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row and row['roll_no']:
                        students.append({
                            'roll_no': row['roll_no'],
                            'name': row['name'],
                            'email': row['email'],
                            'marks': row['marks']
                        })
            return students
        except IOError as e:
            raise StudentRecordError(f"Error reading students: {e}")

    def get_student_by_roll(self, roll_no):
        """Get student by roll number"""
        try:
            with open(self.csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row and row['roll_no'] == str(roll_no):
                        return {
                            'roll_no': row['roll_no'],
                            'name': row['name'],
                            'email': row['email'],
                            'marks': row['marks']
                        }
            raise StudentRecordError(f"Student with roll number {roll_no} not found")
        except IOError as e:
            raise StudentRecordError(f"Error reading student: {e}")

    def update_student(self, roll_no, name=None, email=None, marks=None):
        """Update student record"""
        try:
            students = []
            found = False

            with open(self.csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row and row['roll_no'] == str(roll_no):
                        found = True
                        row['name'] = name or row['name']
                        row['email'] = email or row['email']
                        row['marks'] = marks or row['marks']
                    students.append(row)

            if not found:
                raise StudentRecordError(f"Student with roll number {roll_no} not found")

            with open(self.csv_file, 'w', newline='') as f:
                if students:
                    writer = csv.DictWriter(f, fieldnames=students[0].keys())
                    writer.writeheader()
                    writer.writerows(students)
        except (IOError, StudentRecordError) as e:
            raise StudentRecordError(f"Error updating student: {e}")

    def delete_student(self, roll_no):
        """Delete student record"""
        try:
            students = []
            found = False

            with open(self.csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not (row and row['roll_no'] == str(roll_no)):
                        students.append(row)
                    else:
                        found = True

            if not found:
                raise StudentRecordError(f"Student with roll number {roll_no} not found")

            with open(self.csv_file, 'w', newline='') as f:
                if students:
                    writer = csv.DictWriter(f, fieldnames=['roll_no', 'name', 'email', 'marks'])
                    writer.writeheader()
                    writer.writerows(students)
        except (IOError, StudentRecordError) as e:
            raise StudentRecordError(f"Error deleting student: {e}")

    def search_by_name(self, name):
        """Search students by name"""
        try:
            results = []
            with open(self.csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row and name.lower() in row['name'].lower():
                        results.append({
                            'roll_no': row['roll_no'],
                            'name': row['name'],
                            'email': row['email'],
                            'marks': row['marks']
                        })
            return results
        except IOError as e:
            raise StudentRecordError(f"Error searching students: {e}")
