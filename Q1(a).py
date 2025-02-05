def squareNumbers(n):
    
    if n <= 1:
        return 0
    k = 0
    for i in range(1,n):
        k = k + i**2
    return k 

print("Enter a number:")
n = int(input())
print(squareNumbers(n))

