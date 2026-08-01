
def test_first_moment():
    a, b  = symbols('a, b', positive=True)
    # rectangle
    p1 = Polygon((0, 0), (a, 0), (a, b), (0, b))
    assert p1.first_moment_of_area() == (a*b**2/8, a**2*b/8)
    assert p1.first_moment_of_area((a/3, b/4)) == (-3*a*b**2/32, -a**2*b/9)

    p1 = Polygon((0, 0), (40, 0), (40, 30), (0, 30))
    assert p1.first_moment_of_area() == (4500, 6000)

    # triangle
    p2 = Polygon((0, 0), (a, 0), (a/2, b))
    assert p2.first_moment_of_area() == (4*a*b**2/81, a**2*b/24)
    assert p2.first_moment_of_area((a/8, b/6)) == (-25*a*b**2/648, -5*a**2*b/768)

    p2 = Polygon((0, 0), (12, 0), (12, 30))
    assert p2.first_moment_of_area() == (S(1600)/3, -S(640)/3)

