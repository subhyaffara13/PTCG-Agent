
def test_anewton():
    f = lambda x: (x - 2)**100
    x = findroot(f, 1., solver=ANewton)
    assert abs(f(x)) < eps

