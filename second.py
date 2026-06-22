print("hello world!")
name = input("enter your name:")
print("welcome", name)


fruit = ["apple", "banana", "cherry"]
print(fruit)
print(type(fruit))
for i in fruit:
    print(i)
fruit.insert(2, "orange")
fruit.append("grape")
fruit.remove("banana")
print(fruit)
del fruit[1:3]
print(fruit)


a = int("2")
b = 4.25
print((a) + (b))

first = int(input("enter first number;"))
second = int(input("enter second number;"))
print("the sum of two numbers is", first + second)

a = int(input("side of the square;"))
print("the area of the square is", (a)*(a))

a = int(input("length ;"))
b = int(input("breadth ;"))
print("the area of the rectangle is;", a*b)

a = float(input("enter the first number;"))
b = float(input("enter the second number;"))
print("avg = ", (a + b)/2)



name = "vansh"
age = 18
city = "jind"
print("name:", name)
print("age:", age)
print("city:", city)



a = int(input("enter first number;"))
b = int(input("enter second number;"))
print("the sum of a and b is", a + b)
print("the difference of a and b is", a - b)
print("the product of a and b is :", a*b)
print("the division of a and b is :", a/b)



name = input("enter your name:")
print("welcome", name)


strng = input("enter a name;")
print(len("strng"))
fruits = ["mango","apple","banana","orange","watermaleon"]
fruits.remove("apple","banana","orange")



x = int(input("enter your maths number;"))
y = int(input("enter your science number;"))
z = int(input("enter your english number;"))
print(x+y+z)
avg = float((x+y+z)/2)
print("avg;", avg)





number = int(input("enter a number;"))
if number%2==0:
    print("even")
else:print("odd")




number = int(input("enter a number;"))
if number>0:
    print("positive")
elif number==0:
    print("zero")
else:
    print("negative")



num1 = float(input("enter first number;"))
num2 = float(input("enter second number;"))
if num1>num2:
    print(num1, "is greater than", num2)
elif num2>num1:
    print(num2, "is greater than", num1)
else:
    print("both numbers are equal")



numb1 = float(input("enter first number;"))
numb2 = float(input("enter second number;"))
numb3 = float(input("enter third number;"))
if numb1>numb2 and numb1>numb3:
    print(numb1, "is greatest")
elif numb2>numb1 and numb2>numb3:
    print(numb2, "is greatest")
else:
    print(numb3, "is greatest")




age = int(input("enter your age;"))
if age>=18:
    print("you are eligible to vote")
else:
    print("you are not eligible to vote")



marks = int(input("enter your marks;"))
if marks>=90:
    print("grade A")
elif marks>=80:
    print("grade B")
elif marks>=70:
    print("grade C")
elif marks>=60:
    print("grade D")
else:
    print("grade F")




year = int(input("enter a year;"))
if (year%4==0 and year%100!=0) or (year%400==0):
    print("leap year")
else:
    print("not a leap year")




username = input("enter username;")
password = input("enter password;")
if username=="admin" and password=="password123":
    print("login successful")
else:
    print("invalid username or password")



num = 17
while num <171:
    print(num)
    num+=17

num=1
while num<11:
     print(num)
     num+=1


num1=2
while num1<21:
     print(num1)
     num1+=2


num3=7
while num3<71:
    print(num3)
    num3+=7


num4=10
while num4>0:
     print(num4)
     num4-=1
num = 1234
reverse = 0
while num > 0:
 digit = num % 10
 reverse = reverse * 10 + digit
 num = num // 10
print("Reversed Number =", reverse)


num = int(input("Enter a number: "))
i = 2
is_prime = True
while i < num:
 if num % i == 0:
  is_prime = False
 break
 i += 1
if is_prime and num > 1:
 print("Prime Number")
else:
 print("Not Prime Number")


for i in range(1, 5):
    for j in range(1, 5):
        print("hello")

for i in range(1, 4):
    for j in range(1, 4):
          print(i)


for i in range(1, 4):
    for j in range(1, 4):
          print(j)



for i in range(1, 4):
    for j in range(1, 4):
          print(i*j)



for i in range(1, 4):
    for j in range(1, 4):
         for k in range(1, 4):
             print(i*j*k)
    
