
students_file = "students.txt"
courses_file = "courses.txt"
lecturers_file = "lecturers.txt"
modules_file = "modules.txt"
grades_file = "grades.txt"
attendance_file = "attendance.txt"
enrollments_file = "enroll.txt"

def initialize_files():
    for filename in [students_file, courses_file, lecturers_file, modules_file, grades_file, attendance_file, enrollments_file]:
        try:
            open(filename, "a").close()
        except Exception as e:
            print(f"Error initializing file {filename}: {e}")

# User Passwords
user_credentials = {
    "administrator": {
        "admin": "admin123"
    },
    "lecturer": {
        "lecturer": "lecturer123"
    },
    "student": {
        "student": "student123"
    },
    "registrar": {
        "registrar": "registrar123"
    },
    "accountant": {
        "accountant": "accountant123"
    }
}

def login(role):
    print(f"\n--- {role.capitalize()} Login ---")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    if username in user_credentials[role] and user_credentials[role][username] == password:
        print(f"Login successful! Welcome, {username}!")
        return True
    else:
        print("Invalid username or password. Please try again.")
        return False

# Main Menu
def main_menu():
    while True:
        print("\nWelcome to University Management System (UMS)")
        print("Select Your Role:")
        print("1. Administrator")
        print("2. Lecturer")
        print("3. Student")
        print("4. Registrar")
        print("5. Accountant")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            if login("administrator"):
                administrator_menu()
        elif choice == "2":
            if login("lecturer"):
                lecturer_main()
        elif choice == "3":
            if login("student"):
                student_id = input("Enter your Student ID: ").strip()
                student_name = validate_student_id(student_id)
                if student_name:
                    student_menu(student_id, student_name)
                else:
                    print("Invalid Student ID. Please try again.")
        elif choice == "4":
            if login("registrar"):
                register_menu()
        elif choice == "5":
            if login("accountant"):
                accountant_menu()
        elif choice == "6":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Administrator Program Role 1:----------------------------------------------------------------------------------------------------- start of admin code
def administrator_menu():
    while True:
        print("\n--- Administrator Menu ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Students")
        print("4. Remove Student")
        print("5. Add Course")
        print("6. View Courses")
        print("7. Add Lecturer")
        print("8. View Lecturers")
        print("9. Update Lecturer")
        print("10. Generate Reports")
        print("11. Search Student")
        print("12. Return to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            remove_student()
        elif choice == "5":
            add_course()
        elif choice == "6":
            view_courses()
        elif choice == "7":
            add_lecturer()
        elif choice == "8":
            view_lecturers()
        elif choice == "9":
            update_lecturers()
        elif choice == "10":
            generate_reports()
        elif choice == "11":
            search_student()
        elif choice == "12":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 12.")

def add_student():
    try:
        open(students_file, "r").close()
    except FileNotFoundError:
        with open(students_file, "w"):
            pass

    student_id = input("Enter Student ID (letters and/or numbers): ").strip()
    if not student_id:
        print("Error: Student ID cannot be empty.")
        return

    with open(students_file, "r") as file:
        students = file.readlines()
        for student in students:
            fields = student.strip().split(",")
            if len(fields) >= 1 and fields[0] == student_id:
                print("Error: Student ID already exists.")
                return

    name = input("Enter Student Name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return

    department = input("Enter Student Department: ").strip()
    if not department:
        print("Error: Department cannot be empty.")
        return

    with open(students_file, "r+") as file:
        file.seek(0, 2)
        if file.tell() > 0:
            file.seek(file.tell() - 1)
            if file.read(1) != "\n":
                file.write("\n")

    with open(students_file, "a") as file:
        file.write(f"{student_id},{name},{department},\n")
    print("Student added successfully.")

def view_students():
    try:
        with open(students_file, "r") as file:
            students = file.readlines()

        if not students:
            print("No students found")
            return

        print("\nStudents:")
        for student in students:
            fields = student.strip().split(",")
            if len(fields) != 4:
                print(f"Malformed entry: {student.strip()}")
                continue
            student_id, name, department, course_code = fields
            print(f"ID: {student_id} | Name: {name} | Department: {department} | Course Code: {course_code}")
    except Exception as e:
        print(f"Error viewing students: {e}")

def remove_student():
    student_id = input("Enter Student ID to remove: ").strip()

    try:
        with open(students_file, "r") as file:
            students = file.readlines()

        updated_students = [student for student in students if not student.startswith(student_id + ",")]

        if len(updated_students) == len(students):
            print("Student ID not found.")
            return

        with open(students_file, "w") as file:
            file.writelines(updated_students)

        print("Student removed successfully.")
    except Exception as e:
        print(f"Error removing student: {e}")

def add_course():
    try:
        open(courses_file, "r").close()
    except FileNotFoundError:
        with open(courses_file, "w"):
            pass

    course_code = input("Enter Course Code: ").strip()
    if not course_code:
        print("Error: Course Code cannot be empty.")
        return

    name = input("Enter Course Name: ").strip()
    if not name:
        print("Error: Course Name cannot be empty.")
        return

    credits = input("Enter Course Credits: ").strip()
    if not credits.isdigit() or int(credits) <= 0:
        print("Error: Credits must be a positive integer.")
        return

    try:
        with open(courses_file, "r") as file:
            courses = file.readlines()

        for course in courses:
            fields = course.strip().split(",")
            if len(fields) >= 3 and fields[0].strip() == course_code:
                print("Error: Course Code already exists.")
                return

    except FileNotFoundError:
        print("Courses file not found. A new file will be created.")

    with open(courses_file, "a") as file:
        if courses:
            file.write("\n")
        file.write(f"{course_code},{name},{credits} credits")
    print("Course added successfully.")

def view_courses():
    try:
        with open(courses_file, "r") as file:
            courses = file.readlines()

        if not courses:
            print("No courses found.")
            return

        print("\nCourses:")
        for course in courses:
            fields = course.strip().split(",")
            if len(fields) != 3:
                print(f"Malformed entry: {course.strip()}")
                continue
            course_code, name, credits = fields
            print(f"Code: {course_code.strip()} | Name: {name.strip()} | Credits: {credits.strip()}")
    except FileNotFoundError:
        print("Courses file not found.")
    except Exception as e:
        print(f"Error viewing courses: {e}")

def add_lecturer():
    try:
        open(lecturers_file, "r").close()
    except FileNotFoundError:
        with open(lecturers_file, "w"):
            pass

    # Get and validate lecturer details
    lecturer_id = input("Enter Lecturer ID: ").strip()
    if not lecturer_id:
        print("Error: Lecturer ID cannot be empty.")
        return

    name = input("Enter Lecturer Name: ").strip()
    if not name:
        print("Error: Lecturer Name cannot be empty.")
        return

    department = input("Enter Lecturer Department: ").strip()
    if not department:
        print("Error: Lecturer Department cannot be empty.")
        return

    email = input("Enter Lecturer Email: ").strip()
    if not email or "@" not in email or "." not in email:
        print("Error: Invalid email address.")
        return

    try:
        with open(lecturers_file, "r") as file:
            lecturers = file.readlines()

        for lecturer in lecturers:
            if lecturer.startswith(lecturer_id + ","):
                print("Error: Lecturer ID already exists.")
                return
    except FileNotFoundError:
        print("Lecturers file not found. A new file will be created.")

    with open(lecturers_file, "a") as file:
        if lecturers:
            file.write("\n")
        file.write(f"{lecturer_id},{name},{department},{email}")
    print("Lecturer added successfully.")

def view_lecturers():
    try:
        with open(lecturers_file, "r") as file:
            lecturers = file.readlines()

        if not lecturers:
            print("No lecturers found.")
            return

        print("\nLecturers:")
        for lecturer in lecturers:
            fields = lecturer.strip().split(",")
            if len(fields) != 4:
                print(f"Malformed entry: {lecturer.strip()}")
                continue
            lecturer_id, name, department, email = fields
            print(f"ID: {lecturer_id.strip()} | Name: {name.strip()} | Department: {department.strip()} | Email: {email.strip()}")
    except FileNotFoundError:
        print("Lecturers file not found.")
    except Exception as e:
        print(f"Error viewing lecturers: {e}")

def update_lecturers():
    lecturer_id = input("Enter Lecturer ID to edit: ").strip()

    try:
        with open(lecturers_file, "r") as file:
            lecturers = file.readlines()

        updated_lecturers = []
        found = False

        for lecturer in lecturers:
            if lecturer.startswith(lecturer_id + ","):
                found = True
                current_id, current_name, current_department, current_email = lecturer.strip().split(",")
                print("\nCurrent Information:")
                print(f"ID: {current_id}")
                print(f"Name: {current_name}")
                print(f"Department: {current_department}")
                print(f"Email: {current_email}")

                print("\nEnter new information (leave blank to keep current):")
                new_name = input("New name: ").strip() or current_name
                new_department = input("New department: ").strip() or current_department
                new_email = input("New email: ").strip() or current_email

                updated_lecturers.append(f"{current_id},{new_name},{new_department},{new_email}\n")
                print("Lecturer updated successfully.")
            else:
                updated_lecturers.append(lecturer)

        if not found:
            print("Lecturer ID not found.")
            return

        with open(lecturers_file, "w") as file:
            file.writelines(updated_lecturers)

    except Exception as e:
        print(f"Error editing lecturer: {e}")

def generate_reports():
    try:
        total_students = sum(1 for _ in open(students_file))
        total_courses = sum(1 for _ in open(courses_file))
        total_lecturers = sum(1 for _ in open(lecturers_file))

        print("\n=== Reports ===")
        print(f"Total Students: {total_students}")
        print(f"Total Courses: {total_courses}")
        print(f"Total Lecturers: {total_lecturers}")
    except Exception as e:
        print(f"Error generating reports: {e}")

def search_student():
    search_term = input("Enter search term (Student ID, Name, or Department): ").strip().lower()

    try:
        with open(students_file, "r") as file:
            students = file.readlines()

        if not students:
            print("No students found.")
            return

        found_students = []
        for student in students:
            fields = student.strip().split(",")
            if len(fields) != 4:
                print(f"Malformed entry: {student.strip()}")
                continue

            student_id, name, department, course_code = fields
            if search_term in student_id.lower() or search_term in name.lower() or search_term in department.lower():
                found_students.append(f"ID: {student_id}, Name: {name}, Department: {department}, Course Code: {course_code}")

        if found_students:
            print("\nSearch Results:")
            for student in found_students:
                print(student)
        else:
            print("No students match your search term.")
    except Exception as e:
        print(f"Error searching students: {e}")

def update_student():
    student_id = input("Enter Student ID to edit: ").strip()

    try:
        with open(students_file, "r") as file:
            students = file.readlines()

        updated_students = []
        found = False

        for student in students:
            fields = student.strip().split(",")
            if len(fields) != 4:
                print(f"Malformed entry: {student.strip()}")
                continue

            current_id, current_name, current_department, current_course_code = fields

            if current_id == student_id:
                found = True
                print("\nCurrent Information: ")
                print(f"ID: {current_id}")
                print(f"Name: {current_name}")
                print(f"Department: {current_department}")
                print(f"Course Code: {current_course_code}")

                print("\nEnter new information (leave blank to keep current):")
                new_id = input("New ID: ").strip() or current_id
                new_name = input("New Name: ").strip() or current_name
                new_department = input("New Department: ").strip() or current_department
                new_course_code = input("New Course Code: ").strip() or current_course_code

                updated_students.append(f"{new_id},{new_name},{new_department},{new_course_code}\n")
                print("Student updated successfully")
            else:
                updated_students.append(student)

        if not found:
            print("Student ID not found.")
            return

        with open(students_file, "w") as file:
            file.writelines(updated_students)

    except Exception as e:
        print(f"Error editing student: {e}") #---------------------------------------------------------------------------------------------------- end of admin code



#Accountant Program Role 5: ----------------------------------------------------------------------------- start of accountant code
from datetime import datetime

def file_record_setup(record_file, student_file, payment_guide_file):
    existing_student_ids = set()
    try:
        record_file.seek(0)
        record_file_lines = record_file.readlines()
        for line in record_file_lines:
            line = line.strip()
            record_file_column = line.split(',')
            record_file_student_id = record_file_column[0]
            existing_student_ids.add(record_file_student_id)
    except FileNotFoundError:
        pass

    students = student_file.readlines()
    payment_guide_lines = payment_guide_file.readlines()
    for line_student_file in students:
        line_student_file = line_student_file.strip()
        student_file_column = line_student_file.split(',')
        student_id = student_file_column[0]
        student_name = student_file_column[1]

        if len(student_file_column) < 4 or student_file_column[3] == '':
            student_coursecode = ''
            if student_id not in existing_student_ids:
                data_list = [student_id, student_name, student_coursecode, 'COURSE NOT ASSIGNED TO STUDENT']
                record_file.write(','.join(data_list) + '\n')
                existing_student_ids.add(student_id)
            continue
        student_coursecode = student_file_column[3].strip()

        if student_id not in existing_student_ids:
            course_found = False
            for line_payment_guide in payment_guide_lines:
                line_payment_guide = line_payment_guide.strip()
                payment_guide_column = line_payment_guide.split(',')
                payment_coursecode = payment_guide_column[0].strip()
                payment_courseamount = payment_guide_column[1].strip()
                if student_coursecode == payment_coursecode:
                    data_list = [student_id, student_name, payment_coursecode, payment_courseamount,
                                 'unpaid,unpaid,unpaid,unpaid']
                    record_file.write(','.join(data_list) + '\n')
                    existing_student_ids.add(student_id)  # Add student_id to avoid future duplicates
                    course_found = True
                    break
            if not course_found:
                data_list = [student_id, student_name, student_coursecode, 'COURSE NOT FOUND']
                record_file.write(','.join(data_list) + '\n')
                existing_student_ids.add(student_id)
    return existing_student_ids


# CHECK AVAILABLE STUDENT Validation
def existing_studentid(check_id, existing_student_ids):
    if check_id not in existing_student_ids:
        print("\n Student ID does not exist, Please enter the correct Format")
        return False
    return True


# find & print student with no(not assigned/invalid) course id
def print_invalid_students(record_file_column, line):
    if "COURSE NOT FOUND" in line:
        print("STUDENT WITH INVALID COURSE ID  FOR STUDENT:")
        print(record_file_column[0], record_file_column[1], record_file_column[2])
    if "COURSE NOT ASSIGNED TO STUDENT" in line:
        print("COURSE NOT ASSIGNED TO STUDENT", record_file_column[0], record_file_column[1])


# CHECK AVAILABLE STUDENT DETAILS No.1
def check_student_details(record_file, existing_student_ids):
    while True:
        record_file.seek(0)
        print('-' * 5)
        check_id = input("Please enter student ID: TP")
        check_id = "TP" + check_id
        if existing_studentid(check_id, existing_student_ids):
            for line in record_file:
                line = line.strip()
                record_file_column = line.split(',')
                searchcolumn = record_file_column[0]

                if check_id == searchcolumn:
                    callout_banner(f'STUDENT with ID {check_id}')
                    if len(record_file_column) == 8:
                        print("Name of Student:", record_file_column[1])
                        print("Student ID Number:", record_file_column[0])
                        print("Student's Course Code:", record_file_column[2])
                        print("Student's Course Fee: MYR", record_file_column[3], record_file_column[4])
                        print("Student's Medical Fee MYR 500 Status:", record_file_column[5])
                        print("Student Visa Application Fee MYR 1500 Status:", record_file_column[6])
                        print("Student Registration Fee MYR 300 Status:", record_file_column[7], end="")
                    else:
                        print("Name of Student:", record_file_column[1])
                        print("Student ID Number:", record_file_column[0])
                        print("Student's Course Code:", record_file_column[2])
                        print(record_file_column[3], )

        while True:
            user_input = input("\n Continue checking for another student?(Y/N)")
            if user_input.upper() == "Y":
                break
            elif user_input.upper() == "N":
                return
            else:
                print("invalid input, please enter 'Y' or 'N': ")


# STUDENT WITH OUTSTANDING FEES No.2
def view_student_with_outstanding_fees(record_file):
    while True:
        callout_banner("View Student with Outstanding Fees")
        print("1. Student with any outstanding fees")
        print("2. Student with Course Fee Outstanding")
        print("3. Student with Medical Fee Outstanding")
        print("4. Student with Visa Application Fee Outstanding")
        print("5. Student with Registration Fee Outstanding")
        outstanding = input("Please enter your choice 1/2/3/4/5:")
        record_file.seek(0)
        count = 0
        print_banner = False
        for line in record_file:
            line = line.strip()
            record_file_column = line.split(',')
            if not print_banner:
                callout_banner("Student with CourseFee Outstanding")
                print_banner = True

            if outstanding == "1":
                if len(record_file_column) == 8 and "unpaid" in line:
                    count += 1
                    print(count, "Name of Student:", record_file_column[0])
                    print("Student ID Number:", record_file_column[1])
                    print("Student's Course Code:", record_file_column[2])
                    print("Student's Course Fee: MYR", record_file_column[3], record_file_column[4])
                    print("Student's Medical Fee MYR 500 Status:", record_file_column[5])
                    print("Student Visa Application Fee MYR 1500 Status:", record_file_column[6])
                    print("Student Registration Fee MYR 300 Status:", record_file_column[7], end="")
                    print("\n", '-' * 5)

                elif len(record_file_column) < 8:
                    print_invalid_students(record_file_column, line)
                    continue

            elif outstanding == "2":
                if len(record_file_column) == 8 and "unpaid" in record_file_column[4]:
                    count += 1
                    print(count, "Name of Student:", record_file_column[0])
                    print("Student ID Number:", record_file_column[1])
                    print("Student's Course Code:", record_file_column[2], ", amount MYR", record_file_column[3],record_file_column[4])
                    print("\n", '-' * 5)
                elif len(record_file_column) < 8:
                    print_invalid_students(record_file_column, line)
                    print("No payment details of Course Fee available before enrolling")
                    continue

            elif outstanding == "3":
                if len(record_file_column) == 8 and "unpaid" in record_file_column[5]:
                    count += 1
                    print(count, "Student:", record_file_column[0], record_file_column[1], "Course Code:",record_file_column[2])
                    print("Student's Medical Fee MYR 500, Status:", record_file_column[5])
                    print("\n", '-' * 5)
                elif len(record_file_column) < 8:
                    print_invalid_students(record_file_column, line)
                    print("No payment details of Medical Fees available before enrolling")
                    continue

            elif outstanding == "4":
                if len(record_file_column) == 8 and "unpaid" in record_file_column[6]:
                    count += 1
                    print(count, "Name of Student:", record_file_column[0], record_file_column[1], "Course Code:",record_file_column[2])
                    print("Student Visa Application Fee MYR 1500, Status:", record_file_column[6])
                    print("\n", '-' * 5)
                elif len(record_file_column) < 8:
                    print_invalid_students(record_file_column, line)
                    print("No payment details of Visa Application available before enrolling")
                    continue

            elif outstanding == "5":
                if len(record_file_column) == 8 and "unpaid" in record_file_column[7]:
                    count += 1
                    print(count, "Name of Student:", record_file_column[0], record_file_column[1], "Course Code:",record_file_column[2])
                    print("Student Registration Fee MYR 300, Status:", record_file_column[7], end="")
                    print("\n", '-' * 5)
                elif len(record_file_column) < 8:
                    print_invalid_students(record_file_column, line)
                    print("No payment details of Registering available before enrolling")
                    continue
        while True:
            user_input = input("\n View another category?(Y/N)")
            if user_input.upper() == "Y":
                break
            elif user_input.upper() == "N":
                return
            else:
                print("invalid input, please enter 'Y' or 'N': ")


# Update Student Payment Record No. 3
def update_payment_record(record_file, existing_student_ids):
    callout_banner("Update Student Payment Record")
    while True:
        record_file.seek(0)
        check_id = input("Please enter student ID: TP")
        check_id = "TP" + check_id
        if existing_studentid(check_id, existing_student_ids):
            lines = record_file.readlines()
            updated = False
            for i, line in enumerate(lines):
                line = line.strip()
                record_file_column = line.split(',')

                if len(record_file_column) == 8 and check_id == record_file_column[0]:
                    print("Name of Student:", record_file_column[1])
                    studentname = record_file_column[1]
                    print("Student ID Number:", record_file_column[0])
                    studentid = record_file_column[0]
                    print("Student's Course Code:", record_file_column[2])
                    print("Student's Course Fee: MYR", record_file_column[3], record_file_column[4])
                    course_fee_amount = record_file_column[3]
                    print("Student's Medical Fee MYR 500 Status:", record_file_column[5])
                    print("Student Visa Application Fee MYR 1500 Status:", record_file_column[6])
                    print("Student Registration Fee MYR 300 Status:", record_file_column[7])
                    print("\n", '-' * 5)

                    print("Which payment record do you wish to update")
                    print("1. Course Fee")
                    print("2. Medical Fee")
                    print("3. Visa Application Fee")
                    print("4. Registration Fee")
                    update_choice = input("Please enter 1/2/3/4 :")

                    if update_choice == "1":
                        confirm = input(f'MYR{course_fee_amount} is this amount received? (Y/N):')
                        if confirm.upper() == "Y":
                            record_file_column[4] = "paid"
                            updated = True
                            print(f'Course fee MYR{course_fee_amount} PAID by {studentid} {studentname}')
                    elif update_choice == "2":
                        confirm = input(f'Is Medical Fee MYR 500 received for {studentid} {studentname} (Y/N):')
                        if confirm.upper() == "Y":
                            record_file_column[5] = "paid"
                            updated = True
                            print(f'Medical Fee amount MYR 500 PAID by {studentid} {studentname}')
                    elif update_choice == "3":
                        confirm = input(f'Is Visa Application Fee amount MYR 1500 received for {studentid} {studentname} (Y/N):')
                        if confirm.upper() == "Y":
                            record_file_column[6] = "paid"
                            updated = True
                            print(f'Medical Fee MYR 500 PAID by {studentid} {studentname}')
                    elif update_choice == "4":
                        confirm = input(f'Is Registration Fee amount MYR 300 received for {studentid} {studentname} (Y/N):')
                        if confirm.upper() == "Y":
                            record_file_column[7] = "paid"
                            updated = True
                            print(f'Registration Fee MYR 300 PAID by {studentid} {studentname}')
                    if updated:
                        lines[i] = ",".join(record_file_column) + "\n"
                    break

                elif len(record_file_column) < 8 and check_id == record_file_column[0]:
                    print_invalid_students(record_file_column, line)
                    print("No available payment record, please enroll student to course")
                    break
            if updated:
                record_file.seek(0)
                record_file.truncate()
                record_file.writelines(lines)
                record_file.seek(0)
                print("\n Record Updated")
            else:
                print("~ No update was made")

        user_input = input("\n Continue updating records?(Y/N)")
        if user_input.upper() == "Y":
            continue
        elif user_input.upper() == "N":
            return
        else:
            print("invalid input, please enter 'Y' or 'N': ")


# FINANCIAL RECEIPT No.4
def generate_receipts(record_file, existing_student_ids):
    callout_banner("Issue Receipts")
    while True:
        check_id = input("Please enter student ID: TP")
        check_id = "TP" + check_id
        if existing_studentid(check_id, existing_student_ids):
            record_file.seek(0)
            lines = record_file.readlines()
            for line in lines:
                line = line.strip()
                record_file_column = line.split(',')
                if len(record_file_column) == 8 and check_id == record_file_column[0]:
                    studentid = record_file_column[0]
                    studentname = record_file_column[1]
                    studentcourse = record_file_column[2]
                    studentcourse_amount = float(record_file_column[3].replace(' ', ''))
                    studentcourse_status = record_file_column[4]
                    studentmedical_status = record_file_column[5]
                    studentvisa_status = record_file_column[6]
                    studentregistration_status = record_file_column[7]

                    total_paid, total_unpaid = calculation(studentcourse_amount, studentcourse_status,
                                                           studentmedical_status, studentvisa_status,
                                                           studentregistration_status)

                    filename = f'{studentid} Financial Receipt.txt'
                    current_date = datetime.now()
                    current_date = current_date.strftime("%y-%m-%d")
                    with open(filename, 'w') as file:
                        details = f"""
                        ----------------------------------
                        Digital Receipt for {studentid}
                        ----------------------------------
                        Name of Student: {studentid}
                        Student ID Number: {studentname}
                        Student's Course Code: {studentcourse}
                        Student's Course Fee: MYR {studentcourse_amount} {studentcourse_status}
                        Student's Medical Fee MYR 500 Status: {studentmedical_status}
                        Student Visa Application Fee MYR 1500 Status: {studentvisa_status}
                        Student Registration Fee MYR 300 Status: {studentregistration_status}

                        Date Receipt issued {current_date}
                        Total Paid : MYR {total_paid}
                        ----------------------------------
                        """
                        file.write(details)

                    print(details)
                    print(f'Receipt for {studentid} generated and saved to {filename}')
                    break

                elif len(record_file_column) < 8 and check_id == record_file_column[0]:
                    print_invalid_students(record_file_column, line)
                    print("Receipt not issued, please enroll student to course")
                    break

        while True:
            user_input = input("\nDo you wish to issue another receipt? (Y/N): ")
            if user_input.upper() == "Y":
                break
            elif user_input.upper() == "N":
                return
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")


# Calculate Total Paid & Unpaid amount for No.4 & No.5
def calculation(studentcourse_amount, studentcourse_status, studentmedical_status, studentvisa_status,studentregistration_status):
    try:
        studentcourse_amount = float(studentcourse_amount)

        total_paid = sum([
            studentcourse_amount if studentcourse_status == 'paid' else 0,
            500 if studentmedical_status == 'paid' else 0,
            1500 if studentvisa_status == 'paid' else 0,
            300 if studentregistration_status == 'paid' else 0
        ])

        total_unpaid = sum([
            studentcourse_amount if studentcourse_status == 'unpaid' else 0,
            500 if studentmedical_status == 'unpaid' else 0,
            1500 if studentvisa_status == 'unpaid' else 0,
            300 if studentregistration_status == 'unpaid' else 0
        ])

        return total_paid, total_unpaid

    except ValueError:
        print("Error: Please check the student payment status and ensure amounts are valid.")
        return 0, 0


# VIEW STUDENT OVERALL FINANCIAL SUMMARY
def view_student_financial_summary(record_file, existing_student_ids):
    callout_banner("View Student Financial Summary")
    while True:
        check_id = input("Please enter student ID: TP")
        check_id = "TP" + check_id
        if existing_studentid(check_id, existing_student_ids):
            record_file.seek(0)
            lines = record_file.readlines()
            student_found = True
            for line in lines:
                line = line.strip()
                record_file_column = line.split(',')
                if len(record_file_column) == 8 and check_id == record_file_column[0]:
                    studentid = record_file_column[0]
                    studentname = record_file_column[1]
                    studentcourse = record_file_column[2]
                    studentcourse_amount = float(record_file_column[3].replace(' ', ''))
                    studentcourse_status = record_file_column[4]
                    studentmedical_status = record_file_column[5]
                    studentvisa_status = record_file_column[6]
                    studentregistration_status = record_file_column[7]

                    total_paid, total_unpaid = calculation(studentcourse_amount, studentcourse_status,
                                                           studentmedical_status, studentvisa_status,
                                                           studentregistration_status)

                    callout_banner(f' Financial Summary of {check_id}')
                    print(studentid, studentname, studentcourse)
                    print('-' * 5, "\nUnpaid:")
                    if studentcourse_status == "unpaid":
                        print("Course Fee: MYR", studentcourse_amount)
                    if studentmedical_status == "unpaid":
                        print("Medical Fee MYR 500")
                    if studentvisa_status == "unpaid":
                        print("Visa Application Fee MYR 1500")
                    if studentregistration_status == "unpaid":
                        print("Registration Fee MYR 300")
                    if studentcourse_status != "unpaid" and studentmedical_status != "unpaid" and studentvisa_status != "unpaid" and studentregistration_status != "unpaid":
                        print("(No Outstanding Payments)")

                    print('-' * 5, "\nPaid:")
                    if studentcourse_status == "paid":
                        print("Course Fee: MYR", studentcourse_amount)
                    if studentmedical_status == "paid":
                        print("Medical Fee MYR 500")
                    if studentvisa_status == "paid":
                        print("Visa Application Fee MYR 1500")
                    if studentregistration_status == "paid":
                        print("Registration Fee MYR 300")
                    if studentcourse_status != "paid" and studentmedical_status != "paid" and studentvisa_status != "paid" and studentregistration_status != "paid":
                        print(" (No Payment made)")

                    print("\nTotal Paid : MYR", total_paid)
                    print("Total Unpaid: MYR", total_unpaid)
                    student_found = True
                    break
                elif len(record_file_column) < 8 and check_id == record_file_column[0]:
                    print_invalid_students(record_file_column, line)
                    student_found = False
                    break

            if not student_found:
                print("Please enroll student to course")

        while True:
            user_input = input("\nDo you wish to view another student's summary? (Y/N): ")
            if user_input.upper() == "Y":
                break
            elif user_input.upper() == "N":
                return
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")


# CALLOUT BANNER
def callout_banner(title):
    width = len(title) + 10
    print(''.strip())
    print('-' * width)
    print(f'  {title}  ')
    print('-' * width)


# STARTUP_ACTIONS
def accountant_menu():
    with open('students.txt', 'r') as student_file, open('payment_guide.txt', 'r') as payment_guide_file, open(
            'student_payment_record.txt', 'r+') as record_file:
        existing_student_ids = file_record_setup(record_file, student_file, payment_guide_file)
        while True:
            callout_banner("LIST OF ACTIONS")
            print("1. Check Student Details")
            print("2. View student with outstanding fees")
            print("3. Update Payment Record")
            print("4. Issue receipts")
            print("5. View financial summary")
            print("6. Return to Main Menu")

            choice = input("Enter your choice (1/2/3/4/5/6): ")
            file_record_setup(record_file, student_file, payment_guide_file)
            if choice == "1":
                check_student_details(record_file, existing_student_ids)

            elif choice == "2":
                view_student_with_outstanding_fees(record_file)

            elif choice == "3":
                update_payment_record(record_file, existing_student_ids)

            elif choice == "4":
                generate_receipts(record_file, existing_student_ids)

            elif choice == "5":
                view_student_financial_summary(record_file, existing_student_ids)

            elif choice == "6":
                print("Returning to Main Menu...")
                break

            else:
                print(
                    "\nPlease enter a valid option (1/2/3/4/5/6)")  #--------------------------------------------------------------- end of accountant code

# Student Program Role 3:----------------------------------------------------------------------------------------------------------- start of student code
def validate_student_id(student_id):
    try:
        with open("students.txt", "r") as file:  # Open the students.txt file
            for line in file:
                record = line.strip().split(',')  # Split the line into components
                print(f"Checking student record: {record}")  # Print the record being checked
                if record[0].strip() == student_id:  # Check if the first element (Student ID) matches
                    return True  # Return True if a match is found
        return False  # Return False if no match is found
    except FileNotFoundError:
        print("Error: students.txt file not found.")
        return False  # Return False if the file is not found

# Student Menu Function 1
def student_menu(student_id, student_name):
    student_ids, student_names, student_grades = read_grades_file(grades_file)  # Load grades from file
    while True:
        print("\nWelcome to Student Menu")
        print("1. View Available Modules")
        print("2. Enroll in Module")
        print("3. View Grades")
        print("4. Access Attendance Record")
        print("5. Unenroll from Module")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_available_modules()
        elif choice == "2":
            enroll_student_in_module(student_id, student_name)  # Use the passed student name
        elif choice == "3":
            view_grades(student_id, student_ids, student_names, student_grades)
        elif choice == "4":
            access_attendance_record(student_id)
        elif choice == "5":
            unenroll_from_module(student_id, enrollments_file)
        elif choice == "6":
            break
        else:
            print("Invalid choice, Please try again.")

#Validation for students
def validate_student_id(student_id):
    try:
        with open(students_file, "r") as file:
            for line in file:
                record = line.strip().split(',')
                print(f"Checking student record: {record}")
                if record[0].strip() == student_id:
                    print("Student record found.")
                    return record[1].strip()
        print("No matching student record found.")
        return None
    except FileNotFoundError:
        print("Error: students.txt file not found.")
        return None

# View Available Modules 2
def view_available_modules():
    try:
        # Open and read the modules file
        with open(modules_file, "r") as file:
            modules = file.read().strip()
            if modules:  # If the file is not empty, display modules
                print("\nAvailable Modules:")
                print(modules)
            else:
                print("No Modules Available.")  # Message if no modules are available
    except FileNotFoundError:
        print(f"Error: {modules_file} not found.")  # Error if the file is missing


def get_module_data(module_code):
    """Retrieve module data based on the module code."""
    try:
        with open('modules.txt', 'r') as file:  # Replace with your actual module data file
            for line in file:
                data = line.strip().split(', ')
                if data[0] == module_code:
                    return data  # Return the entire line as a list
    except FileNotFoundError:
        print("Error: Module data file not found.")
    return None

# Updated enroll_student_in_module function 3
def enroll_student_in_module(student_id, student_name):
    """Enroll a student in a module."""
    module_code = input("Enter the course code to enroll in the module: ").strip()
    module_data = get_module_data(module_code)

    if module_data is None:
        print(f"No module found with code: {module_code}")
        return

    print(f"\nModule Data for {module_code}:")
    module_description = ", ".join(module_data[2:5])  # Adjust based on your module data structure
    print("Module Description:")
    print(f"- {module_description}")

    student_exists = False
    try:
        with open(students_file, "r") as file:
            for line in file:
                student_info = line.strip().split(",")
                print(f"Checking student record: {student_info}")  # Debugging output
                if student_info[0] == student_id and student_info[1].strip() == student_name:
                    student_exists = True
                    break

        if not student_exists:
            print("Error: Student ID and name do not match any records.")
            return

        with open(enrollments_file, "r") as file:
            enrollments = file.readlines()

        for line in enrollments:
            if student_id in line and module_code in line:
                print(f"Error: Student {student_name} is already enrolled in {module_code}.")
                return

        print("Preparing to write to the enrollment file...")
        enrollment_record = f"{student_id}, {student_name}, {module_description}"
        print(f"Writing to enrollment file: {enrollment_record}")
        with open(enrollments_file, "a") as file:
            file.write(enrollment_record + "\n")

        print(f"Student {student_id} ({student_name}) successfully enrolled in the following module:")
        print(f"- {module_description}")

    except FileNotFoundError:
        print("Error: The required file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to view student grades 4
def read_grades_file(file_path):
    student_ids = []
    student_names = []
    student_grades = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split(', ')
        student_ids.append(parts[0])  # Student ID
        student_names.append(parts[1])  # Student Name
        grades = parts[3:]  # Assuming grades start from the 4th element
        student_grades.append(grades)  # Store grades as a list of lists

    return student_ids, student_names, student_grades

def view_grades(student_id, student_ids, student_names, student_grades):
    if student_id in student_ids:
        index = student_ids.index(student_id)  # Find the index of the student ID
        print(f"\nStudent ID: {student_id}")
        print(f"Name: {student_names[index]}")
        for course in student_grades[index]:
            course_name, grade = course.rsplit(' - ', 1)
            print(f"  {course_name}: {grade}")
    else:
        print("Student ID not found.")

# Function to access attendance records by student ID 5
def access_attendance_record(student_id):
    # Check if the student ID is empty or invalid
    if not student_id.strip():
        print("Please enter a valid student ID.")
        return

    try:
        # Open the file in read mode
        with open(attendance_file, "r") as file:
            found = False  # Flag to track if student is found

            # Loop through each line in the file
            for line in file:  # Check each line in the attendance file
                # Check if the student ID exists in the current line
                if student_id in line:
                    print(f"\nAttendance Record: {line.strip()}")  # Print attendance
                    found = True
                    break  # Stop searching after finding the first match

            # If no match was found, print a message
            if not found:
                answer = input("Student attendance not found. Do you want to retry? (YES/NO): ")
                if answer == "YES":
                    student_id = input("Enter your Student ID: ")  # Retry by calling the function again
                else:
                    print("Exiting Program, Goodbye!")
                    return

    # Handle specific errors
    except FileNotFoundError:
        print("\nAttendance file not found. Please check the file path.")  # Error if file not found
    except ValueError:
        print("\nError: Invalid data format in the attendance file.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

#Function to unenroll from module
def unenroll_from_module(student_id, enrollments_file):
    try:
        with open(enrollments_file, "r") as file:
            lines = file.readlines()

        updated_lines = []
        found_student = False  # Flag to check if the student is found

        for line in lines:
            if student_id in line:
                found_student = True
                information = line.strip().split(', ')
                name = information[1]  # Student name is the second element
                id = information[0]     # Student ID is the first element
                modules_taken = information[2:]  # This will contain the module descriptions

                if not modules_taken:
                    print("You are not enrolled in any modules.")
                    return

                # Display the current enrollment status
                print(f"\nStudent: {name} (ID: {id})")
                print("Currently enrolled modules:")

                # Display module descriptions with numbering
                for index, module in enumerate(modules_taken, start=1):
                    print(f"{index}. {module.strip()}")  # Print each module description with a number

                # Prompt for the module number to unenroll from
                try:
                    module_number = int(input("\nEnter the number of the module you want to unenroll from: ").strip())
                    if module_number < 1 or module_number > len(modules_taken):
                        print("\nInvalid module number. Please try again.")
                        return

                    # Remove the selected module
                    module_to_remove = modules_taken.pop(module_number - 1)  # Adjust for zero-based index
                    print(f"\nSuccessfully unenrolled from {module_to_remove}.")

                except ValueError:
                    print("\nInvalid input. Please enter a number.")
                    return

                # Update the line with the remaining modules
                updated_lines.append(f"{id}, {name}, {', '.join(modules_taken)}\n")
                continue  # Skip to the next line

            updated_lines.append(line)

        if not found_student:
            print("\nStudent ID not found in the enrollment records.")
            return

        # Write the updated lines back to the file
        with open(enrollments_file, "w") as file:
            file.writelines(updated_lines)

    except FileNotFoundError:
        print(f"Error: {enrollments_file} not found.")#------------------------------------------------------------------------------------- student code end


# Registrar Program Role 4 ---------------------------------------------------------------------------------------------------------------- register code start
def loadstudents():
    students = []
    try:
        with open("students.txt", "r") as file:
            for line in file:
                
                data = line.strip().split(",")
                
       
                if len(data) >= 4:
                    student_id = data[0].strip()
                    student_name = data[1].strip()
                    student_department = data[2].strip()
                    course_id = ",".join(data[3:]).strip()  


                    students.append({
                        "id": student_id,
                        "name": student_name,
                        "department": student_department,
                        "course_id": course_id
                    })
                else:
       
                    print(f"Warning: Skipping invalid line: {line.strip()}")
    except FileNotFoundError:
        print("Error: students.txt file not found.")
    return students


# Save student information
def savestudents(students):
    with open("students.txt", "w") as file:
        for student in students:
            file.write(f"{student['id']},{student['name']},{student['department']},{student['course_id']}\n")

# Load Courses information
def loadcourses():
    courses = []
    try:
        with open("courses.txt", "r") as file:
            for line in file:
                course_id, course_name, credit = line.strip().split(",")
                courses.append({
                    "id": course_id,
                    "name": course_name,
                    "credit": credit
                })
    except FileNotFoundError:
        print("Error: courses.txt file not found.")
    return courses

# Load Modules information
def loadModules():
    modules = []
    try:
        with open("enroll.txt", "r") as file:
            for line in file:
                parts = line.strip().split(", ", 2)
                if len(parts) == 3:
                    student_id, student_name, module_list = parts
                    module_items = module_list.split(", ") 
                    modules.append({
                        "id": student_id,
                        "name": student_name,
                        "modules": module_items
                    })
    except FileNotFoundError:
        print("Error: modules.txt file not found.")
    return modules


def savemodules(modules):
    with open("enroll.txt", "w") as file:
        for module in modules:
            file.write(f"{module['id']}, {module['name']}, {', '.join(module['modules'])}\n")


# register new student == 1
def registerstudent():
    students = loadstudents()
    courses = loadcourses()

    while True:
        student_id = input("Enter student ID (must start with 'TP'): ").strip()
        if not student_id.startswith("TP"):
            print("Error: Student ID must start with 'TP'. Please try again.")
            continue
        break

        course_id = input("Enter courseID: ").strip()

    students.append({"id": student_id, "name": student_name, "department": student_department, "course_id": course_id})
    saveStudents(students)
    print(f"Student {student_name} with CourseID {course_id} registered successfully!")

# Update student information == 2 check
def updatestudentrecord():
    students = loadstudents()
    courses = loadcourses()

    while True:
        student_id = input("Enter the student ID to update (must start with 'TP'): ").strip()
        if not student_id.startswith("TP"):
            print("Error: Student ID must start with 'TP'. Please try again.")
            continue

        if not any(student["id"] == student_id for student in students):
            print("Error: Student ID not found. Please try again.")
            continue

        break

    for student in students:
        if student["id"] == student_id:
            print(f"Current Details: ID={student['id']}, Name={student['name']}, Course ID={student['course_id']}")
            new_name = input("Enter new name (leave blank to keep current): ").strip()
            new_department = input("Enter new department (leave blank to keep current): ").strip()
            new_course_id = input("Enter new course ID (leave blank to keep current): ").strip()

            if new_name:
                student["name"] = new_name
            if new_department:
                student["department"] = new_department
            if new_course_id:
                student["course_id"] = new_course_id

            savestudents(students)
            print(f"Student {student_id} record updated successfully!")
            return

# Manage Modules == 3
def managemodules():
    # Load information of students and modules
    modules = loadModules()

    # Insert studentID and Check
    while True:
        student_id = input("Enter the student ID for modules (must start with 'TP'): ").strip()
        if not student_id.startswith("TP"):
            print("Error: Student ID must start with 'TP'. Please try again.")
            continue

        student = next((m for m in modules if m["id"] == student_id), None)
        if not student:
            print("Error: Student ID not found. Please try again.")
            continue

        break

    # Display current modules
    print(f"\nCurrent Modules for {student['name']} ({student['id']}):")
    for module in student["modules"]:
        print(f" - {module}")

    # Add and Delete modules
    updated_modules = set(student["modules"])

    while True:
        action = input("Enter 'add', 'remove', or 'done': ").strip().lower()

        if action == "done":
            break

        elif action == "add":
            module_name = input("Enter the module name to add: ").strip()
            if module_name in updated_modules:
                print(f"Module '{module_name}' is already enrolled.")
            else:
                updated_modules.add(module_name)
                print(f"Module '{module_name}' added successfully.")
            print("Invalid action. Please enter 'add', 'remove', or 'done'.")

        elif action == "remove":
            module_name = input("Enter the module name to remove: ").strip()
            if module_name not in updated_modules:
                print(f"Error: Module '{module_name}' is not currently enrolled.")
            else:
                updated_modules.remove(module_name)
                print(f"Module '{module_name}' removed successfully.")

        else:
            print("Invalid action. Please enter 'add', 'remove', or 'done'.")

    # Update course modules
    student["modules"] = list(updated_modules)

    # Save all modules back to file
    savemodules(modules)

    print("Modules updated successfully!")


# Transcript == 4
def issuetranscript():
    students = loadstudents()
    courses = loadcourses()

    # Insert studentID and Check
    while True:
        student_id = input("Enter the student ID for transcript (must start with 'TP'): ").strip()
        if not student_id.startswith("TP"):
            print("Error: Student ID must start with 'TP'. Please try again.")
            continue

        if not any(student["id"] == student_id for student in students):
            print("Error: Student ID not found. Please try again.")
            continue

        break

    # Insert CourseID and Check
    while True:
        course_id = input("Enter the course ID: ").strip()

        if not any(course["id"] == course_id for course in courses):
            print("Error: Course ID not found. Please try again.")
            continue

        break
    
    # Get student information
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        print("Error: Student information not found!")
        return

    # Get course information
    course = next((c for c in courses if c["id"] == course_id), None)
    if not course:
        print("Error: Course information not found!")
        return

    # Print transcript
    print("\n---- Transcript ----")
    print(f"Student Name: {student['name']}")
    print(f"Student ID: {student['id']}")
    print(f"Course Name: {course['name']}")
    print(f"Course ID: {course['id']}")

    # Display information of credits
    print(f"\nCredits: {course['credit']}")  # Display credits

    print("\nTranscript generation completed successfully!")

def viewstudentinformation():
    students = loadstudents()
    student_id = input("Enter the student ID to view: ").strip()

    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        print(f"\nStudent Details:\nID: {student['id']}\nName: {student['name']}\nDepartment: {student['department']}\nCourse ID: {student['course_id']}")
    else:
        print("Student not found!")

# main menus
def register_menu():
    while True:
        print("\n---- REGISTRAR MENU ----")
        print("1. Register New Student")
        print("2. Update Student Record")
        print("3. Manage Enrolments")
        print("4. Issue Transcript")
        print("5. View Student Information")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            registerstudent()
        elif choice == "2":
            updatestudentrecord()
        elif choice == "3":
            managemodules()
        elif choice == "4":
            issuetranscript()
        elif choice == "5":
            viewstudentinformation()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")#--------------------------------------------------------------------------------- register code end

# Lecturer Program Role 5 ---------------------------------------------------------------------------------------------------------------- register code start
# Function to check if a file exists
def check_file_exists(file_path):
    try:
        with open(file_path, 'r'):
            return True
    except FileNotFoundError:
        print(f"Error: {file_path} does not exist.")
        return False

# Function to get modules for a lecturer
def get_modules_for_lecturer(lecturer_id):
    if not check_file_exists(lecturers_file):
        return []
    try:
        with open(lecturers_file, 'r') as file:
            modules = file.readlines()
            for module in modules:
                if lecturer_id in module:
                    return module.strip().split(',')[2].split(' - ')
    except Exception as e:
        print(f"An error occurred: {e}")
    return []

# Function to select a module from the list
def select_module(modules):
    print("Select a module:")
    for i, module in enumerate(modules, 1):
        print(f"{i}. {module}")
    choice = int(input("Enter your choice: "))
    if 1 <= choice <= len(modules):
        return modules[choice - 1]
    else:
        print("Invalid choice.")
        return None

# Main menu and get user choices
def lecturer_main():
    while True:
        print("\n--- Lecturer Menu ---")
        print("1. View Assigned Modules")
        print("2. Record Grades")
        print("3. View Student List")
        print("4. Track Attendance")
        print("5. View Student Grades")
        print("6. View Attendance Records")
        print("7. Update Attendance")
        print("8. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            view_assigned_modules()
        elif choice == '2':
            record_grades()
        elif choice == '3':
            view_student_list()
        elif choice == '4':
            track_attendance()
        elif choice == '5':
            view_student_grades()
        elif choice == '6':
            view_attendance_records()
        elif choice == '7':
            update_attendance()
        elif choice == '8':
            print('Exiting')
            break
        else:
            print('Invalid Choice')

# Function to view assigned modules
def view_assigned_modules():
    lecturer_id = input("Enter Lecturer ID: ")
    modules = get_modules_for_lecturer(lecturer_id)
    if modules:
        print("Assigned Modules:")
        for module in modules:
            print(module)
    else:
        print("No modules found for this lecturer.")

# Function to record grades
def record_grades():
    lecturer_id = input("Enter Lecturer ID: ")
    modules = get_modules_for_lecturer(lecturer_id)
    if not modules:
        return
    module_code = select_module(modules)
    if not module_code:
        return
    student_id = input("Enter Student ID: ")
    grade = input("Enter Grade: ")
    if not validate_grade(grade):
        print("Invalid grade. Please enter a valid grade (A/B/C/D/F).")
        return

    if not check_file_exists(grades_file):
        return
    try:
        with open(grades_file, 'a') as file:
            file.write(f"{student_id},{module_code},{grade}\n")
            print("Grade recorded successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to validate grades
def validate_grade(grade):
    valid_grades = ['A', 'B', 'C', 'D', 'F']
    return grade.upper() in valid_grades

# Function to view student list
def view_student_list():
    lecturer_id = input("Enter Lecturer ID: ")
    modules = get_modules_for_lecturer(lecturer_id)
    if not modules:
        return
    module_code = select_module(modules)
    if not module_code:
        return
    if not check_file_exists(students_file):
        return
    try:
        with open(students_file, 'r') as file:
            students = file.readlines()
            print(f"Students in {module_code}:")
            for student in students:
                if module_code in student:
                    print(student.strip())
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to track attendance
def track_attendance():
    lecturer_id = input("Enter Lecturer ID: ")
    modules = get_modules_for_lecturer(lecturer_id)
    if not modules:
        return
    module_code = select_module(modules)
    if not module_code:
        return
    student_id = input("Enter Student ID: ")
    attendance = input("Enter Attendance (Present/Absent): ")
    if attendance not in ['Present', 'Absent']:
        print("Invalid attendance. Please enter 'Present' or 'Absent'.")
        return

    if not check_file_exists(attendance_file):
        return

    # Read existing attendance data
    attendance_data = read_file(attendance_file)

    # Check if attendance for this student and module already exists
    existing_entry = None
    for line in attendance_data:
        parts = line.strip().split(',')
        if parts[0] == student_id and parts[1] == module_code:
            existing_entry = line
            break

    # Update or append attendance data
    if existing_entry:
        # Update existing attendance
        attendance_data.remove(existing_entry)
        attendance_data.append(f"{student_id},{module_code},{attendance}\n")
    else:
        # Append new attendance record
        attendance_data.append(f"{student_id},{module_code},{attendance}\n")

    # Write updated attendance data to file
    append_to_file(attendance_file, "".join(attendance_data))

    print("Attendance recorded successfully.")

# Function to view student grades
def view_student_grades():
    lecturer_id = input("Enter Lecturer ID: ")
    modules = get_modules_for_lecturer(lecturer_id)
    if not modules:
        return
    module_code = select_module(modules)
    if not module_code:
        return
    if not check_file_exists(grades_file):
        return
    try:
        with open(grades_file, 'r') as file:
            grades = file.readlines()
            print(f"Grades for {module_code}:")
            for grade in grades:
                if module_code in grade:
                    print(grade.strip())
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to view attendance records
def view_attendance_records():
    lecturer_id = input("Enter Lecturer ID: ")
    modules = get_modules_for_lecturer(lecturer_id)
    if not modules:
        return
    module_code = select_module(modules)
    if not module_code:
        return
    if not check_file_exists(attendance_file):
        return
    try:
        with open(attendance_file, 'r') as file:
            attendance_records = file.readlines()
            print(f"Attendance records for {module_code}:")
            for record in attendance_records:
                if module_code in record:
                    print(record.strip())
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to update attendance
def update_attendance():
    lecturer_id = input("Enter Lecturer ID: ")
    modules = get_modules_for_lecturer(lecturer_id)
    if not modules:
        return
    module_code = select_module(modules)
    if not module_code:
        return
    student_id = input("Enter Student ID: ")
    new_attendance = input("Enter New Attendance (Present/Absent): ")
    if new_attendance not in ['Present', 'Absent']:
        print("Invalid attendance. Please enter 'Present' or 'Absent'.")
        return

    if not check_file_exists(attendance_file):
        return
    try:
        with open(attendance_file, 'r') as file:
            attendance_records = file.readlines()

        with open(attendance_file, 'w') as file:
            for record in attendance_records:
                parts = record.strip().split(',')
                if parts[0] == student_id and parts[1] == module_code:
                    file.write(f"{student_id},{module_code},{new_attendance}\n")
                else:
                    file.write(record)
        print("Attendance updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Error handling
def read_file(file_name):
    try:
        with open(file_name, "r") as file:
            data = file.readlines()
            return data
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        return []

# Function to append data to a file
def append_to_file(file_name, data):
    try:
        with open(file_name, 'a') as file:
            file.write(data+"\n")
    except Exception as e:
        print(f"An error occurred: {e}")#--------------------------------------------------------------------------- lecturer code end

# Run the program
if __name__ == "__main__":
    main_menu()
