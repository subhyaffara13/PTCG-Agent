
def test_director_circle():
    x, y, a, b = symbols('x y a b')
    e = Ellipse((x, y), a, b)
    # the general result
    assert e.director_circle() == Circle((x, y), sqrt(a**2 + b**2))
    # a special case where Ellipse is a Circle
    assert Circle((3, 4), 8).director_circle() == Circle((3, 4), 8*sqrt(2))

