
def test_W20():
    # integral not calculated
    assert (integrate(x**2*polylog(3, 1/(x + 1)), (x, 0, 1)) ==
            -pi**2/36 - R(17, 108) + zeta(3)/4 +
            (-pi**2/2 - 4*log(2) + log(2)**2 + 35/3)*log(2)/9)

