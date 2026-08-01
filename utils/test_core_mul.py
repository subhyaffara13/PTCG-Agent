
def test_core_mul():
    x = Symbol("x")
    for c in (Mul, Mul(x, 4)):
        check(c)

