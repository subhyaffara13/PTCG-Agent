
def test_auxiliary_circle():
    x, y, a, b = symbols('x y a b')
    e = Ellipse((x, y), a, b)
    # the general result
    assert e.auxiliary_circle() == Circle((x, y), Max(a, b))
    # a special case where Ellipse is a Circle
    assert Circle((3, 4), 8).auxiliary_circle() == Circle((3, 4), 8)

