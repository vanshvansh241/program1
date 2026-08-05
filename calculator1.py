# basic calculator with functions
print("======basic calculator=====")
num1= float(input("enter a number: "))
num2= float(input("enter a number: "))
choice= float(input("enter your choice(1-7): "))
def calculator(num1, num2, choice):
    if choice == 1:
        return num1 + num2
    elif choice == 2:
        return num1 - num2
    elif choice == 3:
        return num1 * num2
    elif choice == 4:
        if num2 != 0:
            return num1 / num2
        else:
            return "Error! Division by zero is not allowed."
    elif choice == 5:
        return num1 % num2
    elif choice == 6:
        return num1 ** num2
    elif choice == 7:
        return num1 // num2
    else:
        return "Enter a valid choice"