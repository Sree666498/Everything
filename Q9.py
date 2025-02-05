def count_divisions_by_2(n):
    count = 0
    while n >= 2:
        n = n / 2
        count += 1
    return count - 1

num = int(input("Enter a positive integer greater than 2: "))
if num > 2:
    print("Number of divisions by 2 before getting less than 2:", count_divisions_by_2(num))
else:
    print("Please enter a number greater than 2.")
