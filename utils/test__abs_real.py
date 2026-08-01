
def test_Abs_real():
    # test some properties of abs that only apply
    # to real numbers
    x = Symbol('x', complex=True)
    assert sqrt(x**2) != Abs(x)
    assert Abs(x**2) != x**2

    x = Symbol('x', real=True)
    assert sqrt(x**2) == Abs(x)
    assert Abs(x**2) == x**2

    # if the symbol is zero, the following will still apply
    nn = Symbol('nn', nonnegative=True, real=True)
    np = Symbol('np', nonpositive=True, real=True)
    assert Abs(nn) == nn
    assert Abs(np) == -np

