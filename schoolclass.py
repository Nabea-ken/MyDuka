class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")


class Student(Person):
    def __init__(self, name, age, student_id, course):
        Person.__init__(self, name, age)
        self.student_id = student_id
        self.course = course

    def display_info(self):
        Person.display_info(self)
        print(f"Student ID: {self.student_id}")
        print(f"Course: {self.course}")


class Teacher(Person):
    def __init__(self, name, age, subject, salary):
        Person.__init__(self, name, age)
        self.subject = subject
        self.salary = salary

    def display_info(self):
        Person.display_info(self)
        print(f"Subject: {self.subject}")
        print(f"Salary: {self.salary}")


student1 = Student("Mercury", 20, "SDT1", "Computer Science")
teacher1 = Teacher("Venus", 35, "Mathematics", 75000)

print("=== Student Info ===")
student1.display_info()

print("\n=== Teacher Info ===")
teacher1.display_info()
