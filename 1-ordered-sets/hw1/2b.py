total = 0
for binnum in range(1024):
    s = '{0:010b}'.format(binnum)
    m = [[0 for x in range(5)] for y in range(5)]
    possible_lower_matrices = 1
    for x in range(10):
        if s[x] == "0":
            possible_lower_matrices *= 2
    total += possible_lower_matrices
print(total)
