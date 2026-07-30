# n=1
# while n<=100:
#  print(n)
#  n+=1


# n=100
# while n>=1:
#   print(n)
#   n-=1

# n=7
# while n<=70:
#   print(n)
#   n+=7

# n=int(input("enter a number: "))
# i=1
# while i<=10:
#   print(n*i)
#   i+=1


# num1=[1,4,9,16,25,36,49,64,81,100]
# for i in num1:
#     print(i)

# for i in range(100,0,-1):
#     print(i)
 
# n=int(input("enter a number: "))
# sum=0
# for i in range(1,n+1):
#     sum+=i
# print("sum of  numbers= ",sum)


# n=int(input("enter a number: "))
# sum=0
# i=1
# while i<=n:
#     sum+=i
#     i+=1
# print("sum of  numbers= ",sum)

# n=int(input("enter a number: "))
# fact=1
# i=1
# while i<=n:
#     fact*=i
#     i+=1
# print("factorial of  number= ",fact)


n=int(input("enter a number: "))
fact=1
for i in range(1,n+1):
    fact*=i
print("factorial of  number= ",fact)