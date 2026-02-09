class Parent1:
    def method1(self):
        print("From Parent1")

class Parent2:
    def method2(self):
        print("From Parent2")

class Child(Parent1, Parent2):
    pass

child = Child()
child.method1()
child.method2()


class Grandparent:
    def greet(self): 
        print("I'm the Grandparent!")

class P1(Grandparent):
    def greet(self): 
        print("I'm P1!")

class P2(Grandparent):
    def greet(self): 
        print("I'm P2!")

class Greatgrandchild(P1, P2):
    pass

test = Greatgrandchild()
test.greet()
