
def test_section_modulus_and_polar_second_moment_of_area():
    d = Symbol('d', positive=True)
    c = Circle((3, 7), 8)
    assert c.polar_second_moment_of_area() == 2048*pi
    assert c.section_modulus() == (128*pi, 128*pi)
    c = Circle((2, 9), d/2)
    assert c.polar_second_moment_of_area() == pi*d**3*Abs(d)/64 + pi*d*Abs(d)**3/64
    assert c.section_modulus() == (pi*d**3/S(32), pi*d**3/S(32))

    a, b = symbols('a, b', positive=True)
    e = Ellipse((4, 6), a, b)
    assert e.section_modulus() == (pi*a*b**2/S(4), pi*a**2*b/S(4))
    assert e.polar_second_moment_of_area() == pi*a**3*b/S(4) + pi*a*b**3/S(4)
    e = e.rotate(pi/2) # no change in polar and section modulus
    assert e.section_modulus() == (pi*a**2*b/S(4), pi*a*b**2/S(4))
    assert e.polar_second_moment_of_area() == pi*a**3*b/S(4) + pi*a*b**3/S(4)

    e = Ellipse((a, b), 2, 6)
    assert e.section_modulus() == (18*pi, 6*pi)
    assert e.polar_second_moment_of_area() == 120*pi

    e = Ellipse(Point(0, 0), 2, 2)
    assert e.section_modulus() == (2*pi, 2*pi)
    assert e.section_modulus(Point(2, 2)) == (2*pi, 2*pi)
    assert e.section_modulus((2, 2)) == (2*pi, 2*pi)


def test_section_modulus_and_polar_second_moment_of_area():
    a, b = symbols('a, b', positive=True)
    x, y = symbols('x, y')
    rectangle = Polygon((0, b), (0, 0), (a, 0), (a, b))
    assert rectangle.section_modulus(Point(x, y)) == (a*b**3/12/(-b/2 + y), a**3*b/12/(-a/2 + x))
    assert rectangle.polar_second_moment_of_area() == a**3*b/12 + a*b**3/12

    convex = RegularPolygon((0, 0), 1, 6)
    assert convex.section_modulus() == (Rational(5, 8), sqrt(3)*Rational(5, 16))
    assert convex.polar_second_moment_of_area() == 5*sqrt(3)/S(8)

    concave = Polygon((0, 0), (1, 8), (3, 4), (4, 6), (7, 1))
    assert concave.section_modulus() == (Rational(-6371, 429), Rational(-9778, 519))
    assert concave.polar_second_moment_of_area() == Rational(-38669, 252)

