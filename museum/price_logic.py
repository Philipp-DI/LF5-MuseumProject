base_price: float = 15.00
age: int = int(input("Enter your age: "))
is_member: bool = input("Are you a museum member? (yes/no): ").strip().lower() == "yes"
is_student: bool = input("Are you a student? (yes/no): ").strip().lower() == "yes"

if age >= 65:
    c_price = base_price * 0.75
elif age <= 16:
    c_price = base_price * 0.5
else:
    c_price = base_price
    
if is_member:
    c_price *= 0.9
elif is_student:
    c_price *= 0.9
print(f"The final ticket price is: €{c_price:.2f}")