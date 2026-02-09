import datetime

class Person:
    def __init__(self, name: str, birth_year: int):
        self.name: str = name
        self.birth_year: int = birth_year
        self.theoretical_age: int = datetime.datetime.now().year - birth_year
        
    def __str__(self):
        public = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return "\n".join(f"{k}: {v}" for k, v in public.items())
    
    def get_private_info(self):
        private = {k: v for k, v in self.__dict__.items() if k.startswith("_")}
        return "\n".join(f"{k}: {v}" for k, v in private.items()) if private else "No private info"

class MuseumStaff(Person):
    staff_role: dict = {0: "Administrator", 1: "Curator", 2: "Researcher", 3: "Archivist"}
    
    def __init__(self, name: str, birth_year: int, staff_role: int):
        super().__init__(name, birth_year)
        self._staff_role = self.staff_role[staff_role]

# global variables for testing purposes
person1 = Person("Alice", 1990)
person2 = Person("Bob", 1985)
person3 = MuseumStaff("Karl", 1976, 0)
person4 = MuseumStaff("Jochen", 1878, 3)

# testing outputs
print("printing public info only:\n")
print(person1)
print(person4)
print("-" * 30)
print("printing private info if available:\n")
print(person2.get_private_info())
print(person3.get_private_info())