
def bench_R6():
    "sum(simplify((x+sin(i))/x+(x-sin(i))/x) for i in range(100))"
    sum(simplify((x + sin(i))/x + (x - sin(i))/x) for i in range(100))

