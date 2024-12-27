import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Добавляем данные в таблицу Courses
courses_data = [
    (1, 'python', '2021-07-21', '2021-08-21'),
    (2, 'java', '2021-07-13', '2021-08-16')
]
cursor.executemany('''
INSERT INTO Courses (id, name, time_start, time_end) VALUES (?, ?, ?, ?)
''', courses_data)

# Добавляем данные в таблицу Students
students_data = [
    (1, 'Max', 'Brooks', 24, 'Spb'),
    (2, 'John', 'Stones', 15, 'Spb'),
    (3, 'Andy', 'Wings', 45, 'Manhester'),
    (4, 'Kate', 'Brooks', 34, 'Spb')
]
cursor.executemany('''
INSERT INTO Students (id, name, surname, age, city) VALUES (?, ?, ?, ?, ?)
''', students_data)

# Добавляем данные в таблицу Student_courses
student_courses_data = [
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 2)
]
cursor.executemany('''
INSERT INTO Student_courses (student_id, course_id) VALUES (?, ?)
''', student_courses_data)

connection.commit()

# Запросы для получения данных
# Cтуденты старше 30 лет
cursor.execute('''
SELECT * FROM Students WHERE age > 30
''')
students_over_30 = cursor.fetchall()
print("Студенты старше 30 лет:")
for student in students_over_30:
    print(student)

# Студенты, которые проходят курс по python
cursor.execute('''
SELECT s.* FROM Students s
JOIN Student_courses sc ON s.id = sc.student_id
JOIN Courses c ON sc.course_id = c.id
WHERE c.name = 'python'
''')
students_python = cursor.fetchall()
print("\nСтуденты на курсе по python:")
for student in students_python:
    print(student)

# Студенты, которые проходят курс по python и из Spb
cursor.execute('''
SELECT s.* FROM Students s
JOIN Student_courses sc ON s.id = sc.student_id
JOIN Courses c ON sc.course_id = c.id
WHERE c.name = 'python' AND s.city = 'Spb'
''')
students_python_spb = cursor.fetchall()
print("\nСтуденты на курсе по python из Spb:")
for student in students_python_spb:
    print(student)

connection.close()
