# 🎓 University Management System (UMS)

A Python-based application designed to manage all aspects of university operations including student records, course management, lecturer information, module enrollment, grades, attendance tracking, and student payment processing.

---

## Account Credentials

| Role | Username | Password |
|------|----------|----------|
| Administrator | admin | admin123 |
| Lecturer | lecturer | lecturer123 |
| Student | student | student123 |
| Registrar | registrar | registrar123 |
| Accountant | accountant | accountant123 |

---

## Key Features

### Administrator
- Add, view, update, and remove students
- Manage courses (add and view)
- Manage lecturers (add, view, and update)
- Generate system reports
- Search for students

### Lecturer
- View assigned modules
- Record and update student grades
- Track and update student attendance
- View student list per module

### Student
- View available modules and enroll
- Check grades and attendance records
- Unenroll from modules

### Registrar
- Register new students
- Update student records
- Manage course enrollments
- Issue transcripts
- View student information

### Accountant
- Record and update student payments
- Track payment status (course fee, medical fee, visa fee, registration fee)
- Generate payment receipts
- View outstanding fees and financial summaries

---

## Project Structure
```
UMS/
│
├── main.py                      # Main application entry point
│
├── students.txt                 # Student records
├── courses.txt                  # Course records
├── lecturers.txt                # Lecturer records
├── modules.txt                  # Module records
├── grades.txt                   # Student grades
├── attendance.txt               # Attendance records
├── enroll.txt                   # Enrollment records
├── student_payment_record.txt   # Payment records
└── payment_guide.txt            # Course fee reference
```

---

## How to Run

1. Make sure you have **Python 3.9+** installed.
2. Clone or download this repository.
3. Run the application:
```bash
python main.py
```

4. Select your role from the main menu and log in using the credentials above.

---

## Notes

- All data is stored in plain `.txt` files no database setup required.
- Student IDs must begin with `TP` (e.g. `TP12345`). The system will add the prefix automatically if omitted.
- Payment fees are referenced from `payment_guide.txt`. Make sure courses are assigned to students before processing payments.
- Receipts are saved automatically as `<StudentID>_receipt_<date>.txt`.
