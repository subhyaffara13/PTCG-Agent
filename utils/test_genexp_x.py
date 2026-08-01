
def test_genexp_x():
    e = 1/(1 + sqrt(x))
    assert e.nseries(x, 0, 2) == \
        1 + x - sqrt(x) - sqrt(x)**3 + O(x**2, x)

