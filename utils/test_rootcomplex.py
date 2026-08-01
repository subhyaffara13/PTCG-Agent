
def test_rootcomplex():
    R = Rational
    assert ((+1 + I)**R(1, 2)).expand(
        complex=True) == 2**R(1, 4)*cos(  pi/8) + 2**R(1, 4)*sin(  pi/8)*I
    assert ((-1 - I)**R(1, 2)).expand(
        complex=True) == 2**R(1, 4)*cos(3*pi/8) - 2**R(1, 4)*sin(3*pi/8)*I
    assert (sqrt(-10)*I).as_real_imag() == (-sqrt(10), 0)

