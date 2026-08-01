
def test_X8():
    # Puiseux series (terms with fractional degree):
    # => 1/sqrt(x - 3/2 pi) + (x - 3/2 pi)^(3/2) / 12 + O([x - 3/2 pi]^(7/2))

    # see issue 7167:
    x = symbols('x', real=True)
    assert (series(sqrt(sec(x)), x, x0=pi*3/2, n=4) ==
            1/sqrt(x - pi*R(3, 2)) + (x - pi*R(3, 2))**R(3, 2)/12 +
            (x - pi*R(3, 2))**R(7, 2)/160 + O((x - pi*R(3, 2))**4, (x, pi*R(3, 2))))

