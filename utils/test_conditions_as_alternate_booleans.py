
def test_conditions_as_alternate_booleans():
    a, b, c = symbols('a:c')
    assert Piecewise((x, Piecewise((y < 1, x > 0), (y > 1, True)))
        ) == Piecewise((x, ITE(x > 0, y < 1, y > 1)))

