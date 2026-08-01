
def test_polytopes_intersecting_sides():
    fig5 = Polygon(Point(-4.165, -0.832), Point(-3.668, 1.568),
                   Point(-3.266, 1.279), Point(-1.090, -2.080),
                   Point(3.313, -0.683), Point(3.033, -4.845),
                   Point(-4.395, 4.840), Point(-1.007, -3.328))
    assert polytope_integrate(fig5, x**2 + x*y + y**2) ==\
        S(1633405224899363)/(24*10**12)

    fig6 = Polygon(Point(-3.018, -4.473), Point(-0.103, 2.378),
                   Point(-1.605, -2.308), Point(4.516, -0.771),
                   Point(4.203, 0.478))
    assert polytope_integrate(fig6, x**2 + x*y + y**2) ==\
        S(88161333955921)/(3*10**12)

