a = int(input("Enter the 1st number: "))
b = int(input("Enter the 2nd number: "))
c = int(input("Enter the 3rd number: "))

#checking validity of a+b=c
if a + b == c:
    print("(a + b = c) arithmetic operation is possible.")
else:
    print("(a + b = c) arithmetic operation is not possible.")
#checking validity of b-c=a
if b - c == a:
    print("(b - c = a) arithmetic operation is possible.")
else:
    print("(b - c = a) arithmetic operation is not possible.")
#checking validity of a*b=c
if a * b == c:
    print("(a * b = c) arithmetic operation is possible.")
else:
    print("(a * b = c) arithmetic operation is not possible.")