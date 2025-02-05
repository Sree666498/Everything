def permute(a, l, r):
    if l == r:
        print("".join(a))
    else:
        for i in range(l, r + 1):
            a[l], a[i] = a[i], a[l]  # Swap
            permute(a, l + 1, r)
            a[l], a[i] = a[i], a[l]  # Backtrack


string = "catdog"
n = len(string)
permute(list(string), 0, n - 1)