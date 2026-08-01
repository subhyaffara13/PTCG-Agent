
def test_Add_is_zero():
    x, y = symbols('x y', zero=True)
    assert (x + y).is_zero

    # Issue 15873
    e = -2*I + (1 + I)**2
    assert e.is_zero is None

