
def test_muller():
    f = lambda x: (2 + x)**3 + 2
    x = findroot(f, 1., solver=Muller)
    assert abs(f(x)) < eps

