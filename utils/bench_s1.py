
def bench_S1():
    "e=(x+y+z+1)**7;f=e*(e+1);f.expand()"
    e = (x + y + z + 1)**7
    f = e*(e + 1)
    f.expand()

