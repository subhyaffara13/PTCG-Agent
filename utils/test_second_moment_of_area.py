
def test_second_moment_of_area():
    x, y = symbols('x, y')
    e = Ellipse(Point(0, 0), 5, 4)
    I_yy = 2*4*integrate(sqrt(25 - x**2)*x**2, (x, -5, 5))/5
    I_xx = 2*5*integrate(sqrt(16 - y**2)*y**2, (y, -4, 4))/4
    Y = 3*sqrt(1 - x**2/5**2)
    I_xy = integrate(integrate(y, (y, -Y, Y))*x, (x, -5, 5))
    assert I_yy == e.second_moment_of_area()[1]
    assert I_xx == e.second_moment_of_area()[0]
    assert I_xy == e.second_moment_of_area()[2]
    #checking for other point
    t1 = e.second_moment_of_area(Point(6,5))
    t2 = (580*pi, 845*pi, 600*pi)
    assert t1==t2


def test_second_moment_of_area():
    x, y = symbols('x, y')
    # triangle
    p1, p2, p3 = [(0, 0), (4, 0), (0, 2)]
    p = (0, 0)
    # equation of hypotenuse
    eq_y = (1-x/4)*2
    I_yy = integrate((x**2) * (integrate(1, (y, 0, eq_y))), (x, 0, 4))
    I_xx = integrate(1 * (integrate(y**2, (y, 0, eq_y))), (x, 0, 4))
    I_xy = integrate(x * (integrate(y, (y, 0, eq_y))), (x, 0, 4))

    triangle = Polygon(p1, p2, p3)

    assert (I_xx - triangle.second_moment_of_area(p)[0]) == 0
    assert (I_yy - triangle.second_moment_of_area(p)[1]) == 0
    assert (I_xy - triangle.second_moment_of_area(p)[2]) == 0

    # rectangle
    p1, p2, p3, p4=[(0, 0), (4, 0), (4, 2), (0, 2)]
    I_yy = integrate((x**2) * integrate(1, (y, 0, 2)), (x, 0, 4))
    I_xx = integrate(1 * integrate(y**2, (y, 0, 2)), (x, 0, 4))
    I_xy = integrate(x * integrate(y, (y, 0, 2)), (x, 0, 4))

    rectangle = Polygon(p1, p2, p3, p4)

    assert (I_xx - rectangle.second_moment_of_area(p)[0]) == 0
    assert (I_yy - rectangle.second_moment_of_area(p)[1]) == 0
    assert (I_xy - rectangle.second_moment_of_area(p)[2]) == 0


    r = RegularPolygon(Point(0, 0), 5, 3)
    assert r.second_moment_of_area() == (1875*sqrt(3)/S(32), 1875*sqrt(3)/S(32), 0)

