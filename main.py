class Student:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.__grades = []

    def add_grade(self, grade):
        if 0 <= grade <= 100:
            self.__grades.append(grade)
            print(f"➕ {self.first_name}ga {grade} baho qo'shildi.")
            return True
        print("❌ Baho 0 va 100 oralig'ida bo'lishi kerak.")
        return False

    def remove_grade(self, grade):
        try:
            self.__grades.remove(grade)
            print(f"➖ {grade} baho o'chirildi.")
            return True
        except ValueError:
            print(f"❌ {grade} baho ro'yxatda topilmadi.")
            return False

    def get_average_grade(self):
        if not self.__grades:
            return 0.0
        return sum(self.__grades) / len(self.__grades)
