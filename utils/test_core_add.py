
def test_core_add():
    x = Symbol("x")
    for c in (Add, Add(x, 4)):
        check(c)

