from django.shortcuts import render, redirect
from django.contrib import messages
from .student_manager import StudentRecordManager, Student, StudentRecordError


def index(request):
    """Display student records manager menu"""
    return render(request, 'chapter2_student_records/index.html')


def list_students(request):
    """List all students"""
    try:
        manager = StudentRecordManager()
        students = manager.get_all_students()
        context = {'students': students}
        return render(request, 'chapter2_student_records/list_students.html', context)
    except StudentRecordError as e:
        messages.error(request, str(e))
        return redirect('chapter2_student_records:index')


def add_student(request):
    """Add a new student"""
    if request.method == 'POST':
        try:
            roll_no = request.POST.get('roll_no').strip()
            name = request.POST.get('name').strip()
            email = request.POST.get('email').strip()
            marks = request.POST.get('marks').strip()

            # Validation
            if not all([roll_no, name, email, marks]):
                raise StudentRecordError("All fields are required")

            try:
                marks = float(marks)
                if not (0 <= marks <= 100):
                    raise StudentRecordError("Marks must be between 0 and 100")
            except ValueError:
                raise StudentRecordError("Marks must be a valid number")

            student = Student(roll_no, name, email, marks)
            manager = StudentRecordManager()
            manager.add_student(student)
            messages.success(request, f"Student {name} added successfully")
            return redirect('chapter2_student_records:list_students')
        except StudentRecordError as e:
            messages.error(request, str(e))

    return render(request, 'chapter2_student_records/add_student.html')


def search_student(request):
    """Search student by name"""
    results = []
    if request.method == 'POST':
        try:
            search_term = request.POST.get('search_term', '').strip()
            if not search_term:
                raise StudentRecordError("Please enter a search term")

            manager = StudentRecordManager()
            results = manager.search_by_name(search_term)

            if not results:
                messages.info(request, f"No students found matching '{search_term}'")
        except StudentRecordError as e:
            messages.error(request, str(e))

    return render(request, 'chapter2_student_records/search_student.html', {'results': results})


def update_student(request, roll_no):
    """Update student record"""
    manager = StudentRecordManager()
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            marks = request.POST.get('marks', '').strip()

            if marks:
                try:
                    marks = float(marks)
                    if not (0 <= marks <= 100):
                        raise StudentRecordError("Marks must be between 0 and 100")
                except ValueError:
                    raise StudentRecordError("Marks must be a valid number")

            manager.update_student(roll_no, name if name else None, 
                                  email if email else None, 
                                  marks if marks else None)
            messages.success(request, "Student updated successfully")
            return redirect('chapter2_student_records:list_students')
        except StudentRecordError as e:
            messages.error(request, str(e))
    
    try:
        student = manager.get_student_by_roll(roll_no)
        return render(request, 'chapter2_student_records/update_student.html', {'student': student})
    except StudentRecordError as e:
        messages.error(request, str(e))
        return redirect('chapter2_student_records:list_students')


def delete_student(request, roll_no):
    """Delete student record"""
    try:
        manager = StudentRecordManager()
        student = manager.get_student_by_roll(roll_no)
        
        if request.method == 'POST':
            manager.delete_student(roll_no)
            messages.success(request, f"Student {student['name']} deleted successfully")
            return redirect('chapter2_student_records:list_students')
        
        return render(request, 'chapter2_student_records/delete_student.html', {'student': student})
    except StudentRecordError as e:
        messages.error(request, str(e))
        return redirect('chapter2_student_records:list_students')
