
def test_distribution_over_equality():
    assert Product(Eq(x*2, f(x)), (x, 1, 3)).doit() == Eq(48, f(1)*f(2)*f(3))
    assert Sum(Eq(f(x), x**2), (x, 0, y)) == \
        Eq(Sum(f(x), (x, 0, y)), Sum(x**2, (x, 0, y)))

