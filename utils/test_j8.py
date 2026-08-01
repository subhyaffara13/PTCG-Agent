
def test_J8():
    p = besselj(R(3,2), z)
    q = (sin(z)/z - cos(z))/sqrt(pi*z/2)
    assert simplify(expand_func(p) -q) == 0

