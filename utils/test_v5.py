
def test_V5():
    # Returns (-45*x**2 + 80*x - 41)/(5*sqrt(2*x - 1)*(4*x**2 - 4*x + 1))
    assert (integrate((3*x - 5)**2/(2*x - 1)**R(7, 2), x).simplify() ==
            (-41 + 80*x - 45*x**2)/(5*(2*x - 1)**R(5, 2)))

