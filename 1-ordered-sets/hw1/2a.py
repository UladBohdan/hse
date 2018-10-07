total = 0
for binnum in range(1024): # 1024 = 2^10 - we have 10 binary cells to fill.
    s = '{0:010b}'.format(binnum)
    m = [[0 for x in range(5)] for y in range(5)]
    m[0][1] = s[0]
    m[0][2] = s[1]
    m[0][3] = s[2]
    m[0][4] = s[3]
    m[1][2] = s[4]
    m[1][3] = s[5]
    m[1][4] = s[6]
    m[2][3] = s[7]
    m[2][4] = s[8]
    m[3][4] = s[9]
    valid = True
    for i in range(0,4):
        for j in range(i+1, 5):
            for k in range (j+1, 5):
                if m[i][j] == "1" and m[j][k] == "1" and m[i][k] == "0":
                    valid = False
    if valid == True:
        total += 1
print(total)
