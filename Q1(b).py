def squareOddNumbers(n):
    
    if n <= 1:
        return 0
    n = n // 2
    k = 0
    for i in range(n):
        k = k + (2*i+1)**2
    return k

print("Enter a number:")
n = int(input())
print(squareOddNumbers(n))