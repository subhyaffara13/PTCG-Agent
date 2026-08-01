
def bench_R5():
    "blowup(L, 8); L=uniq(L)"
    def blowup(L, n):
        for i in range(n):
            L.append( (L[i] + L[i + 1]) * L[i + 2] )

    def uniq(x):
        v = set(x)
        return v
    L = [x, y, z]
    blowup(L, 8)
    L = uniq(L)

