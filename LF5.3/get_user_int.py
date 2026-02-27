import math as m

while True:
    user_input = input("Please enter a number: ")
    if user_input.isdigit():
        value = int(user_input)
        print(f"You entered {value}")
    elif user_input.replace('.', '', 1).isdigit() and user_input.count('.') < 2:
        value = float(user_input)
        rounded_value: int = m.ceil(value) if (value - m.floor(value)) >= 0.5 else m.floor(value)
        print(f"You entered {value}, rounded to {rounded_value}")
    else:
        print("Invalid input. Please enter a valid number.")