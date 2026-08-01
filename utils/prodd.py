
def prodd(t, i, j, k):
    res = 1.0
    for s in range(k+2):
        if i + s != j:
            res *= (t[j] - t[i+s])
    return res

