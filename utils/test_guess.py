
def test_guess():
    i0, i1 = symbols('i0 i1')
    assert guess([1, 2, 6, 24, 120], evaluate=False) == [Product(i1 + 1, (i1, 1, i0 - 1))]
    assert guess([1, 2, 6, 24, 120]) == [RisingFactorial(2, i0 - 1)]
    assert guess([1, 2, 7, 42, 429, 7436, 218348, 10850216], niter=4) == [
        2**(i0 - 1)*(Rational(27, 16))**(i0**2/2 - 3*i0/2 +
        1)*Product(RisingFactorial(Rational(5, 3), i1 - 1)*RisingFactorial(Rational(7, 3), i1
        - 1)/(RisingFactorial(Rational(3, 2), i1 - 1)*RisingFactorial(Rational(5, 2), i1 -
        1)), (i1, 1, i0 - 1))]
    assert guess([1, 0, 2]) == []
    x, y = symbols('x y')
    assert guess([1, 2, 6, 24, 120], variables=[x, y]) == [RisingFactorial(2, x - 1)]

