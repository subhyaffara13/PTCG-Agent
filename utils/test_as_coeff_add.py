
def test_as_coeff_add():
    assert (7, (3*x, 4*x**2)) == (7 + 3*x + 4*x**2).as_coeff_add()


def test_as_coeff_add():
    assert S(2).as_coeff_add() == (2, ())
    assert S(3.0).as_coeff_add() == (0, (S(3.0),))
    assert S(-3.0).as_coeff_add() == (0, (S(-3.0),))
    assert x.as_coeff_add() == (0, (x,))
    assert (x - 1).as_coeff_add() == (-1, (x,))
    assert (x + 1).as_coeff_add() == (1, (x,))
    assert (x + 2).as_coeff_add() == (2, (x,))
    assert (x + y).as_coeff_add(y) == (x, (y,))
    assert (3*x).as_coeff_add(y) == (3*x, ())
    # don't do expansion
    e = (x + y)**2
    assert e.as_coeff_add(y) == (0, (e,))

