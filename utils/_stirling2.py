
def _stirling2(n, k):
    row = [0, 1]+[0]*(k-1) # for n = 1
    for i in range(2, n+1):
        for j in range(min(k,i), 0, -1):
            row[j] = j * row[j] + row[j-1]
    return Integer(row[k])

