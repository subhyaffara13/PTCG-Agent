
def test_Poly_termwise():
    f = Poly(x**2 + 20*x + 400)
    g = Poly(x**2 + 2*x + 4)

    def func(monom, coeff):
        (k,) = monom
        return coeff//10**(2 - k)

    assert f.termwise(func) == g

    def func(monom, coeff):
        (k,) = monom
        return (k,), coeff//10**(2 - k)

    assert f.termwise(func) == g

