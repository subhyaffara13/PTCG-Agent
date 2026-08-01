
def test_core_power():
    x = Symbol("x")
    for c in (Pow, Pow(x, 4)):
        check(c)

