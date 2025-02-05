def distinct_Elements(seq):
    if len(seq) == len(set(seq)):
        print("All the elements in the sequence are distinct.")
    else:
        print("All the elements in the sequence are not distinct.")
    
n = int(input("Give me the length of the sequence: "))
seq = []
for i in range(n):
    num = int(input("Give me the number in the sequence: "))
    seq.append(num)
distinct_Elements(seq)