import sqlite3

connection = sqlite3.connect('my_database.db')

cursor = connection.cursor()

# Создаем таблицу Students
cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    age INTEGER NOT NULL,
    city TEXT NOT NULL
)
''')

# Создаем таблицу Courses
cursor.execute('''
CREATE TABLE IF NOT EXISTS Courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    time_start TEXT NOT NULL,
    time_end TEXT NOT NULL
)
''')

# Создаем таблицу Student_courses
cursor.execute('''
CREATE TABLE IF NOT EXISTS Student_courses (
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (course_id) REFERENCES Courses(id),
    PRIMARY KEY (student_id, course_id)
)
''')

connection.commit()
connection.close()

print("База данных и таблицы успешно созданы.")
