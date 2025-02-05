def has_odd_product_pair(seq):
    count = 0
    for i in seq:
        if i % 2 != 0:
            count = count + 1
    '''Basically if there are 2 or more odd numbers it can give 
       pairs of odd numbers whose product will be an odd number'''
    if count >= 2:      
        return True
    else:
        return False

n = int(input("Give me the length of the sequence: "))
seq = []
for i in range(n):
    num = int(input("Give me the number in the sequence: "))
    seq.append(num)

print(has_odd_product_pair(seq))