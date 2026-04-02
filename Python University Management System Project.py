"""
University Management System (UMS)
Roles: Administrator, Lecturer, Student, Registrar, Accountant
"""

from datetime import datetime

# ─────────────────────────────────────────────
# FILE PATHS
# ─────────────────────────────────────────────
STUDENTS_FILE    = "data/students.txt"
COURSES_FILE     = "data/courses.txt"
LECTURERS_FILE   = "data/lecturers.txt"
MODULES_FILE     = "data/modules.txt"
GRADES_FILE      = "data/grades.txt"
ATTENDANCE_FILE  = "data/attendance.txt"
ENROLLMENTS_FILE = "data/enroll.txt"
PAYMENT_RECORD   = "data/student_payment_record.txt"
PAYMENT_GUIDE    = "data/payment_guide.txt"

# ─────────────────────────────────────────────
# CREDENTIALS
# ─────────────────────────────────────────────
USER_CREDENTIALS = {
    "administrator": {"admin":      "admin123"},
    "lecturer":      {"lecturer":   "lecturer123"},
    "student":       {"student":    "student123"},
    "registrar":     {"registrar":  "registrar123"},
    "accountant":    {"accountant": "accountant123"},
}

# ─────────────────────────────────────────────────────────────────────────────
# SHARED UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def initialize_files():
    """Create all required data files if they don't already exist."""
    for path in [STUDENTS_FILE, COURSES_FILE, LECTURERS_FILE, MODULES_FILE,
                 GRADES_FILE, ATTENDANCE_FILE, ENROLLMENTS_FILE,
                 PAYMENT_RECORD, PAYMENT_GUIDE]:
        try:
            open(path, "a").close()
        except OSError as e:
            print(f"Error initializing '{path}': {e}")


def read_lines(filepath):
    """Return a list of stripped, non-empty lines from a file."""
    try:
        with open(filepath, "r") as f:
            return [line.rstrip("\n") for line in f if line.strip()]
    except FileNotFoundError:
        return []


def write_lines(filepath, lines):
    """Overwrite a file with the given list of lines."""
    with open(filepath, "w") as f:
        for line in lines:
            f.write(line if line.endswith("\n") else line + "\n")


def banner(title):
    """Print a simple section banner."""
    bar = "─" * (len(title) + 4)
    print(f"\n{bar}\n  {title}\n{bar}")


def yes_no(prompt):
    """Ask a Y/N question; return True for Y, False for N."""
    while True:
        ans = input(f"{prompt} (Y/N): ").strip().upper()
        if ans == "Y":
            return True
        if ans == "N":
            return False
        print("Please enter 'Y' or 'N'.")


def login(role):
    """Prompt for credentials; return True on success."""
    banner(f"{role.capitalize()} Login")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if USER_CREDENTIALS.get(role, {}).get(username) == password:
        print(f"Login successful! Welcome, {username}.")
        return True
    print("Invalid username or password.")
    return False


# ─────────────────────────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────────────────────────

def main_menu():
    initialize_files()
    options = {
        "1": ("Administrator", administrator_menu),
        "2": ("Lecturer",      lecturer_main),
        "3": ("Student",       None),          # handled inline
        "4": ("Registrar",     register_menu),
        "5": ("Accountant",    accountant_menu),
    }
    while True:
        banner("University Management System (UMS)")
        for key, (label, _) in options.items():
            print(f"  {key}. {label}")
        print("  6. Exit")

        choice = input("Select role: ").strip()

        if choice == "6":
            print("Goodbye!")
            break
        elif choice in options:
            label, func = options[choice]
            role_key = label.lower()
            if not login(role_key):
                continue
            if choice == "3":
                student_id = input("Enter your Student ID: ").strip()
                if not student_id.startswith("TP"):
                    student_id = "TP" + student_id
                student_name = validate_student_id(student_id)
                if student_name:
                    student_menu(student_id, student_name)
                else:
                    print("Invalid Student ID.")
            else:
                func()
        else:
            print("Invalid choice.")


# ─────────────────────────────────────────────────────────────────────────────
# ADMINISTRATOR
# ─────────────────────────────────────────────────────────────────────────────

def administrator_menu():
    actions = {
        "1":  ("Add Student",       add_student),
        "2":  ("View Students",     view_students),
        "3":  ("Update Student",    update_student),
        "4":  ("Remove Student",    remove_student),
        "5":  ("Add Course",        add_course),
        "6":  ("View Courses",      view_courses),
        "7":  ("Add Lecturer",      add_lecturer),
        "8":  ("View Lecturers",    view_lecturers),
        "9":  ("Update Lecturer",   update_lecturer),
        "10": ("Generate Reports",  generate_reports),
        "11": ("Search Student",    search_student),
    }
    while True:
        banner("Administrator Menu")
        for key, (label, _) in actions.items():
            print(f"  {key}. {label}")
        print("  12. Return to Main Menu")

        choice = input("Choice: ").strip()
        if choice == "12":
            break
        elif choice in actions:
            actions[choice][1]()
        else:
            print("Invalid choice (1–12).")


def add_student():
    student_id = input("Student ID: ").strip()
    if not student_id:
        print("Error: Student ID cannot be empty.")
        return
    if not student_id.startswith("TP"):
        student_id = "TP" + student_id

    lines = read_lines(STUDENTS_FILE)
    if any(line.split(",")[0].strip() == student_id for line in lines):
        print("Error: Student ID already exists.")
        return

    name = input("Student Name: ").strip()
    department = input("Department: ").strip()
    if not name or not department:
        print("Error: Name and Department cannot be empty.")
        return

    with open(STUDENTS_FILE, "a") as f:
        f.write(f"{student_id},{name},{department},\n")
    print("Student added successfully.")


def view_students():
    lines = read_lines(STUDENTS_FILE)
    if not lines:
        print("No students found.")
        return
    banner("Students")
    for line in lines:
        fields = line.split(",")
        if len(fields) < 3:
            print(f"  [Malformed] {line}")
            continue
        sid, name, dept = fields[0].strip(), fields[1].strip(), fields[2].strip()
        course = fields[3].strip() if len(fields) > 3 else ""
        print(f"  ID: {sid} | Name: {name} | Dept: {dept} | Course: {course}")


def remove_student():
    student_id = input("Student ID to remove: ").strip()
    if not student_id.startswith("TP"):
        student_id = "TP" + student_id
    
    lines = read_lines(STUDENTS_FILE)
    new_lines = [l for l in lines if not l.strip().startswith(student_id + ",")]
    if len(new_lines) == len(lines):
        print("Student ID not found.")
        return
    write_lines(STUDENTS_FILE, new_lines)
    print("Student removed successfully.")


def update_student():
    student_id = input("Student ID to update: ").strip()
    if not student_id.startswith("TP"):
        student_id = "TP" + student_id
    
    lines = read_lines(STUDENTS_FILE)
    updated, found = [], False

    for line in lines:
        fields = line.split(",")
        if len(fields) < 3:
            updated.append(line)
            continue
        cid = fields[0].strip()
        cname = fields[1].strip()
        cdept = fields[2].strip()
        ccourse = fields[3].strip() if len(fields) > 3 else ""
        
        if cid == student_id:
            found = True
            print(f"\nCurrent → ID: {cid} | Name: {cname} | Dept: {cdept} | Course: {ccourse}")
            print("(Leave blank to keep current value)")
            nid     = input("New ID: ").strip()     or cid
            if not nid.startswith("TP"):
                nid = "TP" + nid
            nname   = input("New Name: ").strip()   or cname
            ndept   = input("New Dept: ").strip()   or cdept
            ncourse = input("New Course: ").strip() or ccourse
            updated.append(f"{nid},{nname},{ndept},{ncourse}")
            print("Student updated.")
        else:
            updated.append(line)

    if not found:
        print("Student ID not found.")
        return
    write_lines(STUDENTS_FILE, updated)


def search_student():
    term = input("Search (ID / Name / Dept): ").strip().lower()
    lines = read_lines(STUDENTS_FILE)
    results = [l for l in lines if term in l.lower()]
    if results:
        banner("Search Results")
        for r in results:
            print(f"  {r}")
    else:
        print("No matching students found.")


def add_course():
    code = input("Course Code: ").strip()
    if not code:
        print("Error: Course Code cannot be empty.")
        return

    lines = read_lines(COURSES_FILE)
    if any(l.split(",")[0].strip() == code for l in lines):
        print("Error: Course Code already exists.")
        return

    name = input("Course Name: ").strip()
    credits = input("Credits: ").strip()
    if not name:
        print("Error: Course Name cannot be empty.")
        return
    if not credits.isdigit() or int(credits) <= 0:
        print("Error: Credits must be a positive integer.")
        return

    with open(COURSES_FILE, "a") as f:
        f.write(f"{code},{name},{credits} credits\n")
    print("Course added successfully.")


def view_courses():
    lines = read_lines(COURSES_FILE)
    if not lines:
        print("No courses found.")
        return
    banner("Courses")
    for line in lines:
        fields = line.split(",")
        if len(fields) != 3:
            print(f"  [Malformed] {line}")
            continue
        print(f"  Code: {fields[0].strip()} | Name: {fields[1].strip()} | Credits: {fields[2].strip()}")


def add_lecturer():
    lid = input("Lecturer ID: ").strip()
    if not lid:
        print("Error: Lecturer ID cannot be empty.")
        return

    lines = read_lines(LECTURERS_FILE)
    if any(l.split(",")[0].strip() == lid for l in lines):
        print("Error: Lecturer ID already exists.")
        return

    name  = input("Lecturer Name: ").strip()
    dept  = input("Department: ").strip()
    email = input("Email: ").strip()
    if not name or not dept:
        print("Error: Name and Department cannot be empty.")
        return
    if not email or "@" not in email or "." not in email:
        print("Error: Invalid email address.")
        return

    with open(LECTURERS_FILE, "a") as f:
        f.write(f"{lid},{name},{dept},{email}\n")
    print("Lecturer added successfully.")


def view_lecturers():
    lines = read_lines(LECTURERS_FILE)
    if not lines:
        print("No lecturers found.")
        return
    banner("Lecturers")
    for line in lines:
        fields = line.split(",")
        if len(fields) != 4:
            print(f"  [Malformed] {line}")
            continue
        print(f"  ID: {fields[0].strip()} | Name: {fields[1].strip()} | Dept: {fields[2].strip()} | Email: {fields[3].strip()}")


def update_lecturer():
    lid = input("Lecturer ID to update: ").strip()
    lines = read_lines(LECTURERS_FILE)
    updated, found = [], False

    for line in lines:
        fields = line.split(",")
        if len(fields) >= 4 and fields[0].strip() == lid:
            found = True
            cid = fields[0].strip()
            cname = fields[1].strip()
            cdept = fields[2].strip()
            cemail = fields[3].strip()
            print(f"\nCurrent → ID: {cid} | Name: {cname} | Dept: {cdept} | Email: {cemail}")
            print("(Leave blank to keep current value)")
            nname  = input("New Name: ").strip()  or cname
            ndept  = input("New Dept: ").strip()  or cdept
            nemail = input("New Email: ").strip() or cemail
            updated.append(f"{cid},{nname},{ndept},{nemail}")
            print("Lecturer updated.")
        else:
            updated.append(line)

    if not found:
        print("Lecturer ID not found.")
        return
    write_lines(LECTURERS_FILE, updated)


def generate_reports():
    banner("Reports")
    print(f"  Total Students : {len(read_lines(STUDENTS_FILE))}")
    print(f"  Total Courses  : {len(read_lines(COURSES_FILE))}")
    print(f"  Total Lecturers: {len(read_lines(LECTURERS_FILE))}")


# ─────────────────────────────────────────────────────────────────────────────
# ACCOUNTANT
# ─────────────────────────────────────────────────────────────────────────────

def _load_payment_records(record_file):
    """Return set of student IDs already in the payment record."""
    existing = set()
    record_file.seek(0)
    for line in record_file:
        cols = line.strip().split(",")
        if cols:
            existing.add(cols[0])
    return existing


def file_record_setup(record_file, student_file, payment_guide_file):
    """Ensure every student in students.txt has a row in the payment record."""
    existing_ids = _load_payment_records(record_file)

    student_file.seek(0)
    payment_guide_file.seek(0)
    payment_guide = {}
    for line in payment_guide_file:
        cols = line.strip().split(",")
        if len(cols) >= 2:
            payment_guide[cols[0].strip()] = cols[1].strip()

    for line in student_file:
        cols = line.strip().split(",")
        if len(cols) < 2:
            continue
        sid, sname = cols[0].strip(), cols[1].strip()
        if sid in existing_ids:
            continue

        course = cols[3].strip() if len(cols) >= 4 else ""
        if not course:
            record_file.write(f"{sid},{sname},,COURSE NOT ASSIGNED TO STUDENT\n")
        elif course in payment_guide:
            amount = payment_guide[course]
            record_file.write(f"{sid},{sname},{course},{amount},unpaid,unpaid,unpaid,unpaid\n")
        else:
            record_file.write(f"{sid},{sname},{course},COURSE NOT FOUND\n")
        existing_ids.add(sid)

    return existing_ids


def _student_id_exists(check_id, existing_ids):
    if check_id not in existing_ids:
        print(f"Student ID '{check_id}' not found.")
        return False
    return True


def _print_invalid_student(cols, line):
    if "COURSE NOT FOUND" in line:
        print(f"  [Invalid course] {cols[0]} {cols[1]} – Course: {cols[2]}")
    elif "COURSE NOT ASSIGNED TO STUDENT" in line:
        print(f"  [No course assigned] {cols[0]} {cols[1]}")


def _print_payment_row(cols):
    """Pretty-print an 8-column payment record."""
    print(f"  Name        : {cols[1]}")
    print(f"  ID          : {cols[0]}")
    print(f"  Course      : {cols[2]}")
    print(f"  Course Fee  : MYR {cols[3]}  [{cols[4]}]")
    print(f"  Medical Fee : MYR 500        [{cols[5]}]")
    print(f"  Visa Fee    : MYR 1500       [{cols[6]}]")
    print(f"  Reg Fee     : MYR 300        [{cols[7]}]")


def check_student_details(record_file, existing_ids):
    while True:
        input_id = input("Student ID (after TP): ").strip()
        sid = input_id if input_id.startswith("TP") else "TP" + input_id
        if _student_id_exists(sid, existing_ids):
            record_file.seek(0)
            for line in record_file:
                cols = line.strip().split(",")
                if cols[0].strip() == sid:
                    banner(f"Student {sid}")
                    if len(cols) == 8:
                        _print_payment_row(cols)
                    else:
                        _print_invalid_student(cols, line)
                    break
        if not yes_no("Check another student?"):
            return


def view_outstanding_fees(record_file):
    fee_labels = {
        "2": ("Course Fee",       4),
        "3": ("Medical Fee",      5),
        "4": ("Visa Fee",         6),
        "5": ("Registration Fee", 7),
    }
    while True:
        banner("Outstanding Fees")
        print("  1. Any outstanding fee")
        print("  2. Course Fee")
        print("  3. Medical Fee")
        print("  4. Visa Application Fee")
        print("  5. Registration Fee")
        opt = input("Choice: ").strip()

        record_file.seek(0)
        count = 0
        for line in record_file:
            cols = line.strip().split(",")
            if len(cols) < 8:
                _print_invalid_student(cols, line)
                continue
            if opt == "1" and "unpaid" in cols[4:]:
                count += 1
                print(f"\n  [{count}]")
                _print_payment_row(cols)
            elif opt in fee_labels:
                _, idx = fee_labels[opt]
                if cols[idx] == "unpaid":
                    count += 1
                    print(f"\n  [{count}] {cols[0]} {cols[1]} | Course: {cols[2]} | Status: unpaid")
        if count == 0:
            print("  No outstanding records for this category.")
        if not yes_no("View another category?"):
            return


def update_payment_record(record_file, existing_ids):
    banner("Update Payment Record")
    fee_map = {
        "1": (4, "Course Fee",       lambda c: f"MYR {c[3]}"),
        "2": (5, "Medical Fee",      lambda _: "MYR 500"),
        "3": (6, "Visa Fee",         lambda _: "MYR 1500"),
        "4": (7, "Registration Fee", lambda _: "MYR 300"),
    }
    while True:
        input_id = input("Student ID (after TP): ").strip()
        sid = input_id if input_id.startswith("TP") else "TP" + input_id
        if not _student_id_exists(sid, existing_ids):
            if not yes_no("Try again?"):
                return
            continue

        record_file.seek(0)
        lines = record_file.readlines()
        updated = False
        for i, line in enumerate(lines):
            cols = line.strip().split(",")
            if cols[0].strip() != sid:
                continue
            if len(cols) < 8:
                _print_invalid_student(cols, line)
                print("  Please enroll the student in a course first.")
                break
            _print_payment_row(cols)
            print("\n  Which fee to update?\n  1. Course  2. Medical  3. Visa  4. Registration")
            choice = input("  Choice: ").strip()
            if choice not in fee_map:
                print("  Invalid choice.")
                break
            idx, label, amount_fn = fee_map[choice]
            if yes_no(f"  Confirm {label} {amount_fn(cols)} received?"):
                cols[idx] = "paid"
                lines[i] = ",".join(cols) + "\n"
                updated = True
                print(f"  {label} marked as PAID for {sid}.")
            break

        if updated:
            record_file.seek(0)
            record_file.truncate()
            record_file.writelines(lines)
            print("  Record saved.")

        if not yes_no("Update another record?"):
            return


def _calculate_totals(cols):
    """Return (total_paid, total_unpaid) from an 8-column payment row."""
    try:
        course_amount = float(cols[3])
    except ValueError:
        return 0.0, 0.0
    fees = [(course_amount, cols[4]), (500.0, cols[5]), (1500.0, cols[6]), (300.0, cols[7])]
    paid   = sum(amt for amt, status in fees if status == "paid")
    unpaid = sum(amt for amt, status in fees if status == "unpaid")
    return paid, unpaid


def generate_receipt(record_file, existing_ids):
    banner("Issue Receipt")
    while True:
        input_id = input("Student ID (after TP): ").strip()
        sid = input_id if input_id.startswith("TP") else "TP" + input_id
        if _student_id_exists(sid, existing_ids):
            record_file.seek(0)
            for line in record_file:
                cols = line.strip().split(",")
                if cols[0].strip() != sid:
                    continue
                if len(cols) < 8:
                    _print_invalid_student(cols, line)
                    print("  Enroll the student in a course before issuing a receipt.")
                    break
                paid, _ = _calculate_totals(cols)
                date_str = datetime.now().strftime("%Y-%m-%d")
                receipt = (
                    f"\n{'─'*40}\n"
                    f"  RECEIPT  –  {date_str}\n"
                    f"{'─'*40}\n"
                    f"  Student   : {cols[1]}  ({cols[0]})\n"
                    f"  Course    : {cols[2]}\n"
                    f"  Course Fee: MYR {cols[3]}  [{cols[4]}]\n"
                    f"  Medical   : MYR 500         [{cols[5]}]\n"
                    f"  Visa      : MYR 1500        [{cols[6]}]\n"
                    f"  Reg Fee   : MYR 300         [{cols[7]}]\n"
                    f"{'─'*40}\n"
                    f"  Total Paid: MYR {paid:.2f}\n"
                    f"{'─'*40}\n"
                )
                print(receipt)
                fname = f"{sid}_receipt_{date_str}.txt"
                with open(fname, "w") as f:
                    f.write(receipt)
                print(f"  Receipt saved to '{fname}'.")
                break
        if not yes_no("Issue another receipt?"):
            return


def view_financial_summary(record_file, existing_ids):
    banner("Financial Summary")
    while True:
        input_id = input("Student ID (after TP): ").strip()
        sid = input_id if input_id.startswith("TP") else "TP" + input_id
        if _student_id_exists(sid, existing_ids):
            record_file.seek(0)
            for line in record_file:
                cols = line.strip().split(",")
                if cols[0].strip() != sid:
                    continue
                if len(cols) < 8:
                    _print_invalid_student(cols, line)
                    break
                paid, unpaid = _calculate_totals(cols)
                banner(f"Financial Summary – {sid}")
                fee_names = ["Course Fee", "Medical Fee (MYR 500)", "Visa Fee (MYR 1500)", "Registration Fee (MYR 300)"]
                statuses  = cols[4:8]
                print("  UNPAID:")
                any_unpaid = any(s == "unpaid" for s in statuses)
                for name, status in zip(fee_names, statuses):
                    if status == "unpaid":
                        print(f"    - {name}")
                if not any_unpaid:
                    print("    (none)")
                print("  PAID:")
                any_paid = any(s == "paid" for s in statuses)
                for name, status in zip(fee_names, statuses):
                    if status == "paid":
                        print(f"    - {name}")
                if not any_paid:
                    print("    (none)")
                print(f"\n  Total Paid  : MYR {paid:.2f}")
                print(f"  Total Unpaid: MYR {unpaid:.2f}")
                break
        if not yes_no("View another student?"):
            return


def accountant_menu():
    # Ensure required files exist before opening
    for path in [STUDENTS_FILE, PAYMENT_GUIDE, PAYMENT_RECORD]:
        open(path, "a").close()

    # Fixed: Compatible with Python 3.9+
    sf = open(STUDENTS_FILE, "r")
    pg = open(PAYMENT_GUIDE, "r")
    rf = open(PAYMENT_RECORD, "r+")
    
    try:
        existing_ids = file_record_setup(rf, sf, pg)

        actions = {
            "1": ("Check Student Details",          lambda: check_student_details(rf, existing_ids)),
            "2": ("View Outstanding Fees",           lambda: view_outstanding_fees(rf)),
            "3": ("Update Payment Record",           lambda: update_payment_record(rf, existing_ids)),
            "4": ("Issue Receipt",                   lambda: generate_receipt(rf, existing_ids)),
            "5": ("View Financial Summary",          lambda: view_financial_summary(rf, existing_ids)),
        }
        while True:
            banner("Accountant Menu")
            for key, (label, _) in actions.items():
                print(f"  {key}. {label}")
            print("  6. Return to Main Menu")
            choice = input("Choice: ").strip()
            if choice == "6":
                break
            elif choice in actions:
                # Refresh existing IDs in case students were added mid-session
                sf.seek(0)
                pg.seek(0)
                existing_ids = file_record_setup(rf, sf, pg)
                actions[choice][1]()
            else:
                print("Invalid choice (1–6).")
    finally:
        sf.close()
        pg.close()
        rf.close()


# ─────────────────────────────────────────────────────────────────────────────
# STUDENT
# ─────────────────────────────────────────────────────────────────────────────

def validate_student_id(student_id):
    """Return the student's name if the ID exists, else None."""
    for line in read_lines(STUDENTS_FILE):
        fields = line.split(",")
        if fields[0].strip() == student_id:
            return fields[1].strip() if len(fields) > 1 else ""
    return None


def student_menu(student_id, student_name):
    actions = {
        "1": ("View Available Modules",  view_available_modules),
        "2": ("Enroll in Module",        lambda: enroll_student(student_id, student_name)),
        "3": ("View Grades",             lambda: view_grades(student_id)),
        "4": ("Access Attendance",       lambda: view_attendance(student_id)),
        "5": ("Unenroll from Module",    lambda: unenroll_from_module(student_id)),
    }
    while True:
        banner(f"Student Menu – {student_name}")
        for key, (label, _) in actions.items():
            print(f"  {key}. {label}")
        print("  6. Back to Main Menu")
        choice = input("Choice: ").strip()
        if choice == "6":
            break
        elif choice in actions:
            actions[choice][1]()
        else:
            print("Invalid choice.")


def view_available_modules():
    lines = read_lines(MODULES_FILE)
    if not lines:
        print("No modules available.")
        return
    banner("Available Modules")
    for line in lines:
        print(f"  {line}")


def _get_module(module_code):
    """Return the module row as a list, or None."""
    for line in read_lines(MODULES_FILE):
        parts = line.split(",")
        if parts[0].strip() == module_code:
            return parts
    return None


def enroll_student(student_id, student_name):
    code = input("Module code to enroll in: ").strip()
    module = _get_module(code)
    if module is None:
        print(f"No module found with code '{code}'.")
        return

    # Check existing enrollment
    for line in read_lines(ENROLLMENTS_FILE):
        parts = line.split(",")
        if len(parts) >= 3 and parts[0].strip() == student_id and code in parts[2]:
            print(f"You are already enrolled in '{code}'.")
            return

    description = ", ".join(p.strip() for p in module[1:] if p.strip())
    with open(ENROLLMENTS_FILE, "a") as f:
        f.write(f"{student_id}, {student_name}, {description}\n")
    print(f"Enrolled in: {description}")


def view_grades(student_id):
    lines = read_lines(GRADES_FILE)
    found = False
    banner(f"Grades – {student_id}")
    for line in lines:
        parts = line.split(",")
        if len(parts) >= 3 and parts[0].strip() == student_id:
            module = parts[1].strip()
            grade  = parts[2].strip()
            print(f"  {module}: {grade}")
            found = True
    if not found:
        print("  No grade records found.")


def view_attendance(student_id):
    lines = read_lines(ATTENDANCE_FILE)
    found = False
    banner(f"Attendance – {student_id}")
    for line in lines:
        parts = line.split(",")
        if len(parts) >= 1 and parts[0].strip() == student_id:
            print(f"  {line}")
            found = True
    if not found:
        print("  No attendance records found.")


def unenroll_from_module(student_id):
    lines = read_lines(ENROLLMENTS_FILE)
    updated = []
    found = False

    for line in lines:
        parts = line.split(", ", 2)
        if len(parts) >= 1 and parts[0].strip() == student_id:
            found = True
            modules = parts[2].split(", ") if len(parts) == 3 else []
            if not modules:
                print("You are not enrolled in any modules.")
                return
            print(f"\nEnrolled modules for {parts[1].strip() if len(parts) > 1 else 'Student'}:")
            for i, m in enumerate(modules, 1):
                print(f"  {i}. {m.strip()}")
            try:
                num = int(input("Enter number to unenroll from: ").strip())
                if not 1 <= num <= len(modules):
                    print("Invalid number.")
                    return
                removed = modules.pop(num - 1)
                print(f"Unenrolled from: {removed.strip()}")
            except ValueError:
                print("Please enter a valid number.")
                return
            if modules:
                updated.append(f"{parts[0]}, {parts[1]}, {', '.join(modules)}")
            # If no modules remain, the student row is simply dropped.
        else:
            updated.append(line)

    if not found:
        print("Student ID not found in enrollment records.")
        return
    write_lines(ENROLLMENTS_FILE, updated)


# ─────────────────────────────────────────────────────────────────────────────
# REGISTRAR
# ─────────────────────────────────────────────────────────────────────────────

def _load_students_as_dicts():
    students = []
    for line in read_lines(STUDENTS_FILE):
        parts = line.split(",")
        if len(parts) >= 3:
            students.append({
                "id":         parts[0].strip(),
                "name":       parts[1].strip(),
                "department": parts[2].strip(),
                "course_id":  parts[3].strip() if len(parts) > 3 else "",
            })
    return students


def _save_students_from_dicts(students):
    write_lines(STUDENTS_FILE,
                [f"{s['id']},{s['name']},{s['department']},{s['course_id']}" for s in students])


def _load_courses_as_dicts():
    courses = []
    for line in read_lines(COURSES_FILE):
        parts = line.split(",")
        if len(parts) == 3:
            courses.append({"id": parts[0].strip(), "name": parts[1].strip(), "credit": parts[2].strip()})
    return courses


def _load_enrollments_as_dicts():
    enrollments = []
    for line in read_lines(ENROLLMENTS_FILE):
        parts = line.split(", ", 2)
        if len(parts) == 3:
            enrollments.append({
                "id":      parts[0].strip(),
                "name":    parts[1].strip(),
                "modules": [m.strip() for m in parts[2].split(", ")],
            })
    return enrollments


def _save_enrollments_from_dicts(enrollments):
    write_lines(ENROLLMENTS_FILE,
                [f"{e['id']}, {e['name']}, {', '.join(e['modules'])}" for e in enrollments])


def _require_tp_prefix():
    while True:
        sid = input("Student ID (with or without TP): ").strip()
        if not sid.startswith("TP"):
            sid = "TP" + sid
        return sid


def register_student():
    students = _load_students_as_dicts()
    sid = _require_tp_prefix()
    if any(s["id"] == sid for s in students):
        print("Error: Student ID already exists.")
        return
    name  = input("Student Name: ").strip()
    dept  = input("Department: ").strip()
    cid   = input("Course ID: ").strip()
    if not name or not dept:
        print("Error: Name and Department cannot be empty.")
        return
    students.append({"id": sid, "name": name, "department": dept, "course_id": cid})
    _save_students_from_dicts(students)
    print(f"Student '{name}' registered successfully.")


def update_student_record():
    students = _load_students_as_dicts()
    while True:
        sid = _require_tp_prefix()
        if any(s["id"] == sid for s in students):
            break
        print("Student ID not found.")

    for s in students:
        if s["id"] == sid:
            print(f"\nCurrent → ID: {s['id']} | Name: {s['name']} | Dept: {s['department']} | Course: {s['course_id']}")
            print("(Leave blank to keep current value)")
            s["name"]       = input("New Name: ").strip()       or s["name"]
            s["department"] = input("New Department: ").strip() or s["department"]
            s["course_id"]  = input("New Course ID: ").strip()  or s["course_id"]
            _save_students_from_dicts(students)
            print("Record updated.")
            return


def manage_enrollments():
    enrollments = _load_enrollments_as_dicts()
    while True:
        sid = _require_tp_prefix()
        entry = next((e for e in enrollments if e["id"] == sid), None)
        if entry:
            break
        print("Student ID not found in enrollment records.")

    print(f"\nModules for {entry['name']} ({entry['id']}):")
    for m in entry["modules"]:
        print(f"  - {m}")

    module_set = set(entry["modules"])
    while True:
        action = input("\n'add' / 'remove' / 'done': ").strip().lower()
        if action == "done":
            break
        elif action == "add":
            m = input("Module name to add: ").strip()
            if m in module_set:
                print(f"'{m}' is already enrolled.")
            else:
                module_set.add(m)
                print(f"'{m}' added.")
        elif action == "remove":
            m = input("Module name to remove: ").strip()
            if m not in module_set:
                print(f"'{m}' is not enrolled.")
            else:
                module_set.remove(m)
                print(f"'{m}' removed.")
        else:
            print("Enter 'add', 'remove', or 'done'.")

    entry["modules"] = sorted(module_set)
    _save_enrollments_from_dicts(enrollments)
    print("Enrollment updated.")


def issue_transcript():
    students = _load_students_as_dicts()
    courses  = _load_courses_as_dicts()

    while True:
        sid = _require_tp_prefix()
        if any(s["id"] == sid for s in students):
            break
        print("Student ID not found.")

    while True:
        cid = input("Course ID: ").strip()
        if any(c["id"] == cid for c in courses):
            break
        print("Course ID not found.")

    student = next(s for s in students if s["id"] == sid)
    course  = next(c for c in courses  if c["id"] == cid)

    banner("Transcript")
    print(f"  Student : {student['name']} ({student['id']})")
    print(f"  Course  : {course['name']} ({course['id']})")
    print(f"  Credits : {course['credit']}")
    print("\nTranscript generated successfully.")


def view_student_information():
    students = _load_students_as_dicts()
    sid = input("Student ID: ").strip()
    if not sid.startswith("TP"):
        sid = "TP" + sid
    student = next((s for s in students if s["id"] == sid), None)
    if student:
        banner("Student Information")
        print(f"  ID         : {student['id']}")
        print(f"  Name       : {student['name']}")
        print(f"  Department : {student['department']}")
        print(f"  Course ID  : {student['course_id']}")
    else:
        print("Student not found.")


def register_menu():
    actions = {
        "1": ("Register New Student",   register_student),
        "2": ("Update Student Record",  update_student_record),
        "3": ("Manage Enrolments",      manage_enrollments),
        "4": ("Issue Transcript",       issue_transcript),
        "5": ("View Student Info",      view_student_information),
    }
    while True:
        banner("Registrar Menu")
        for key, (label, _) in actions.items():
            print(f"  {key}. {label}")
        print("  6. Return to Main Menu")
        choice = input("Choice: ").strip()
        if choice == "6":
            break
        elif choice in actions:
            actions[choice][1]()
        else:
            print("Invalid choice (1–6).")


# ─────────────────────────────────────────────────────────────────────────────
# LECTURER
# ─────────────────────────────────────────────────────────────────────────────

def _get_lecturer_modules(lecturer_id):
    """Return a list of module codes assigned to the lecturer."""
    for line in read_lines(LECTURERS_FILE):
        if line.startswith(lecturer_id + ","):
            parts = line.split(",")
            if len(parts) >= 3:
                return [m.strip() for m in parts[2].split(" - ") if m.strip()]
    return []


def _pick_module(lecturer_id):
    modules = _get_lecturer_modules(lecturer_id)
    if not modules:
        print("No modules found for this lecturer.")
        return None
    print("Modules:")
    for i, m in enumerate(modules, 1):
        print(f"  {i}. {m}")
    try:
        idx = int(input("Select module number: ").strip()) - 1
        if 0 <= idx < len(modules):
            return modules[idx]
    except ValueError:
        pass
    print("Invalid selection.")
    return None


def view_assigned_modules():
    lid = input("Lecturer ID: ").strip()
    modules = _get_lecturer_modules(lid)
    if modules:
        banner(f"Modules – {lid}")
        for m in modules:
            print(f"  {m}")
    else:
        print("No modules found.")


def record_grades():
    lid = input("Lecturer ID: ").strip()
    module = _pick_module(lid)
    if not module:
        return
    sid   = input("Student ID: ").strip()
    if not sid.startswith("TP"):
        sid = "TP" + sid
    grade = input("Grade (A/B/C/D/F): ").strip().upper()
    if grade not in {"A", "B", "C", "D", "F"}:
        print("Invalid grade.")
        return
    with open(GRADES_FILE, "a") as f:
        f.write(f"{sid},{module},{grade}\n")
    print("Grade recorded.")


def view_student_list():
    lid = input("Lecturer ID: ").strip()
    module = _pick_module(lid)
    if not module:
        return
    banner(f"Students in {module}")
    found = False
    for line in read_lines(STUDENTS_FILE):
        parts = line.split(",")
        if len(parts) >= 4 and module in parts[3]:
            print(f"  {line}")
            found = True
    if not found:
        print("  No students found for this module.")


def track_attendance():
    lid = input("Lecturer ID: ").strip()
    module = _pick_module(lid)
    if not module:
        return
    sid    = input("Student ID: ").strip()
    if not sid.startswith("TP"):
        sid = "TP" + sid
    status = input("Attendance (Present/Absent): ").strip().capitalize()
    if status not in {"Present", "Absent"}:
        print("Invalid attendance status.")
        return

    lines = read_lines(ATTENDANCE_FILE)
    new_lines = []
    updated = False
    for line in lines:
        parts = line.split(",")
        if len(parts) >= 2 and parts[0].strip() == sid and parts[1].strip() == module:
            new_lines.append(f"{sid},{module},{status}")
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        new_lines.append(f"{sid},{module},{status}")
    write_lines(ATTENDANCE_FILE, new_lines)
    print("Attendance recorded.")


def view_student_grades():
    lid = input("Lecturer ID: ").strip()
    module = _pick_module(lid)
    if not module:
        return
    banner(f"Grades – {module}")
    found = False
    for line in read_lines(GRADES_FILE):
        parts = line.split(",")
        if len(parts) >= 3 and parts[1].strip() == module:
            print(f"  {line}")
            found = True
    if not found:
        print("  No grades found.")


def view_attendance_records():
    lid = input("Lecturer ID: ").strip()
    module = _pick_module(lid)
    if not module:
        return
    banner(f"Attendance – {module}")
    found = False
    for line in read_lines(ATTENDANCE_FILE):
        parts = line.split(",")
        if len(parts) >= 2 and parts[1].strip() == module:
            print(f"  {line}")
            found = True
    if not found:
        print("  No attendance records found.")


def update_attendance():
    lid = input("Lecturer ID: ").strip()
    module = _pick_module(lid)
    if not module:
        return
    sid    = input("Student ID: ").strip()
    if not sid.startswith("TP"):
        sid = "TP" + sid
    status = input("New Attendance (Present/Absent): ").strip().capitalize()
    if status not in {"Present", "Absent"}:
        print("Invalid attendance status.")
        return

    lines = read_lines(ATTENDANCE_FILE)
    new_lines, updated = [], False
    for line in lines:
        parts = line.split(",")
        if len(parts) >= 2 and parts[0].strip() == sid and parts[1].strip() == module:
            new_lines.append(f"{sid},{module},{status}")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        print("No existing record found to update. Use 'Track Attendance' to add a new record.")
        return
    write_lines(ATTENDANCE_FILE, new_lines)
    print("Attendance updated.")


def lecturer_main():
    actions = {
        "1": ("View Assigned Modules",  view_assigned_modules),
        "2": ("Record Grades",          record_grades),
        "3": ("View Student List",      view_student_list),
        "4": ("Track Attendance",       track_attendance),
        "5": ("View Student Grades",    view_student_grades),
        "6": ("View Attendance Records",view_attendance_records),
        "7": ("Update Attendance",      update_attendance),
    }
    while True:
        banner("Lecturer Menu")
        for key, (label, _) in actions.items():
            print(f"  {key}. {label}")
        print("  8. Return to Main Menu")
        choice = input("Choice: ").strip()
        if choice == "8":
            break
        elif choice in actions:
            actions[choice][1]()
        else:
            print("Invalid choice (1–8).")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main_menu()
