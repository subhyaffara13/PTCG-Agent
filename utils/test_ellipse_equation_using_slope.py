
def test_ellipse_equation_using_slope():
    from sympy.abc import x, y

    e1 = Ellipse(Point(1, 0), 3, 2)
    assert str(e1.equation(_slope=1)) == str((-x + y + 1)**2/8 + (x + y - 1)**2/18 - 1)

    e2 = Ellipse(Point(0, 0), 4, 1)
    assert str(e2.equation(_slope=1)) == str((-x + y)**2/2 + (x + y)**2/32 - 1)

    e3 = Ellipse(Point(1, 5), 6, 2)
    assert str(e3.equation(_slope=2)) == str((-2*x + y - 3)**2/20 + (x + 2*y - 11)**2/180 - 1)

