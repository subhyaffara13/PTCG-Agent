
def test_circumference():
    M = Symbol('M')
    m = Symbol('m')
    assert Ellipse(Point(0, 0), M, m).circumference == 4 * M * elliptic_e((M ** 2 - m ** 2) / M**2)

    assert Ellipse(Point(0, 0), 5, 4).circumference == 20 * elliptic_e(S(9) / 25)

    # circle
    assert Ellipse(None, 1, None, 0).circumference == 2*pi

    # test numerically
    assert abs(Ellipse(None, hradius=5, vradius=3).circumference.evalf(16) - 25.52699886339813) < 1e-10

