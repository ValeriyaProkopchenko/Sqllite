import peewee as pw

db = pw.SqliteDatabase('my_database.db')

# Определяем модели
class BaseModel(pw.Model):
    class Meta:
        database = db

class Student(BaseModel):
    name = pw.CharField()
    surname = pw.CharField()
    age = pw.IntegerField()
    city = pw.CharField()

class Course(BaseModel):
    name = pw.CharField()
    time_start = pw.DateField()
    time_end = pw.DateField()

class StudentCourse(BaseModel):
    student = pw.ForeignKeyField(Student, backref='courses')
    course = pw.ForeignKeyField(Course, backref='students')

class DatabaseManager:
    def __init__(self):
        # Создаем таблицы
        db.connect()
        db.create_tables([Student, Course, StudentCourse], safe=True)
        if not self.is_filled():
            self.populate_data()

    def is_filled(self):
        """Проверяет, заполнены ли таблицы данными."""
        return Student.select().count() > 0

    def populate_data(self):
        """Заполняет таблицы начальными данными."""
        courses_data = [
            {'name': 'python', 'time_start': '2021-07-21', 'time_end': '2021-08-21'},
            {'name': 'java', 'time_start': '2021-07-13', 'time_end': '2021-08-16'}
        ]
        
        students_data = [
            {'name': 'Max', 'surname': 'Brooks', 'age': 24, 'city': 'Spb'},
            {'name': 'John', 'surname': 'Stones', 'age': 15, 'city': 'Spb'},
            {'name': 'Andy', 'surname': 'Wings', 'age': 45, 'city': 'Manhester'},
            {'name': 'Kate', 'surname': 'Brooks', 'age': 34, 'city': 'Spb'}
        ]
        
        student_courses_data = [
            (1, 1),
            (2, 1),
            (3, 1),
            (4, 2)
        ]

        # Вставляем курсы
        for course in courses_data:
            Course.create(**course)

        # Вставляем студентов
        for student in students_data:
            Student.create(**student)

        # Вставляем связи между студентами и курсами
        for student_id, course_id in student_courses_data:
            StudentCourse.create(student=student_id, course=course_id)

    def execute_query(self, query):
        """Выполняет произвольный SQL-запрос и возвращает результаты."""
        return db.execute_sql(query).fetchall()

    def get_students_over_30(self):
        """Получает всех студентов старше 30 лет."""
        return Student.select().where(Student.age > 30)

    def get_students_in_python_course(self):
        """Получает всех студентов на курсе по Python."""
        return (Student
                .select()
                .join(StudentCourse)
                .join(Course)
                .where(Course.name == 'python'))

    def get_students_in_python_course_from_spb(self):
        """Получает всех студентов на курсе по Python из Spb."""
        return (Student
                .select()
                .join(StudentCourse)
                .join(Course)
                .where((Course.name == 'python') & (Student.city == 'Spb')))

    def close(self):
        """Закрывает соединение с базой данных."""
        db.close()


# Тестирование функционала
if __name__ == "__main__":
    db_manager = DatabaseManager()

    print("Студенты старше 30 лет:")
    for student in db_manager.get_students_over_30():
        print(student.name, student.surname)

    print("\nСтуденты на курсе по Python:")
    for student in db_manager.get_students_in_python_course():
        print(student.name, student.surname)

    print("\nСтуденты на курсе по Python из Spb:")
    for student in db_manager.get_students_in_python_course_from_spb():
        print(student.name, student.surname)

    db_manager.close()
