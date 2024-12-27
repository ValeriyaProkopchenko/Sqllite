import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name='my_database.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()
        if not self.is_filled():
            self.populate_data()

    def create_tables(self):
        """Создает таблицы в базе данных."""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            age INTEGER NOT NULL,
            city TEXT NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            time_start TEXT NOT NULL,
            time_end TEXT NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student_courses (
            student_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES Students(id),
            FOREIGN KEY (course_id) REFERENCES Courses(id),
            PRIMARY KEY (student_id, course_id)
        )
        ''')
        
        self.connection.commit()

    def is_filled(self):
        """Проверяет, заполнены ли таблицы данными."""
        self.cursor.execute('SELECT COUNT(*) FROM Students')
        student_count = self.cursor.fetchone()[0]
        return student_count > 0

    def populate_data(self):
        """Заполняет таблицы начальными данными."""
        courses_data = [
            (1, 'python', '2021-07-21', '2021-08-21'),
            (2, 'java', '2021-07-13', '2021-08-16')
        ]
        
        students_data = [
            (1, 'Max', 'Brooks', 24, 'Spb'),
            (2, 'John', 'Stones', 15, 'Spb'),
            (3, 'Andy', 'Wings', 45, 'Manhester'),
            (4, 'Kate', 'Brooks', 34, 'Spb')
        ]
        
        student_courses_data = [
            (1, 1),
            (2, 1),
            (3, 1),
            (4, 2)
        ]
        
        self.cursor.executemany('''
        INSERT INTO Courses (id, name, time_start, time_end) VALUES (?, ?, ?, ?)
        ''', courses_data)

        self.cursor.executemany('''
        INSERT INTO Students (id, name, surname, age, city) VALUES (?, ?, ?, ?, ?)
        ''', students_data)

        self.cursor.executemany('''
        INSERT INTO Student_courses (student_id, course_id) VALUES (?, ?)
        ''', student_courses_data)

        self.connection.commit()

    def execute_query(self, query):
        """Выполняет произвольный SQL-запрос и возвращает результаты."""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_students_over_30(self):
        """Получает всех студентов старше 30 лет."""
        return self.execute_query('SELECT * FROM Students WHERE age > 30')

    def get_students_in_python_course(self):
        """Получает всех студентов на курсе по Python."""
        query = '''
        SELECT s.* FROM Students s
        JOIN Student_courses sc ON s.id = sc.student_id
        JOIN Courses c ON sc.course_id = c.id
        WHERE c.name = 'python'
        '''
        return self.execute_query(query)

    def get_students_in_python_course_from_spb(self):
        """Получает всех студентов на курсе по Python из Spb."""
        query = '''
        SELECT s.* FROM Students s
        JOIN Student_courses sc ON s.id = sc.student_id
        JOIN Courses c ON sc.course_id = c.id
        WHERE c.name = 'python' AND s.city = 'Spb'
        '''
        return self.execute_query(query)

    def close(self):
        self.connection.close()


# Тестирование функционала
if __name__ == "__main__":
    db_manager = DatabaseManager()

    print("Студенты старше 30 лет:")
    for student in db_manager.get_students_over_30():
        print(student)

    print("\nСтуденты на курсе по Python:")
    for student in db_manager.get_students_in_python_course():
        print(student)

    print("\nСтуденты на курсе по Python из Spb:")
    for student in db_manager.get_students_in_python_course_from_spb():
        print(student)

    db_manager.close()
