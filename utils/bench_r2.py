
def bench_R2():
    "Hermite polynomial hermite(15, y)"
    def hermite(n, y):
        if n == 1:
            return 2*y
        if n == 0:
            return 1
        return (2*y*hermite(n - 1, y) - 2*(n - 1)*hermite(n - 2, y)).expand()

    hermite(15, y)

