import datetime

class Person:
    def __init__(self, name: str, birth_year: int):
        self.name: str = name
        self.birth_year: int = birth_year
        self.theoretical_age: int = datetime.datetime.now().year - birth_year


class MuseumStaff(Person):
    staff_role: dict = {0: "Administrator", 2: "Researcher", 3: "Archivist"}
    
    def __init__(self, name: str, birth_year: int, staff_role: int):
        super().__init__(name, birth_year)
        self.staff_role = self.staff_role[staff_role]


# global variables for testing purposes
person1 = Person("Alice", 1990)
person2 = Person("Bob", 1985)
person3 = MuseumStaff("Karl", 1976, 0)
