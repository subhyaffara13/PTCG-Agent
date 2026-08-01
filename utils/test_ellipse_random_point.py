
def test_ellipse_random_point():
    y1 = Symbol('y1', real=True)
    e3 = Ellipse(Point(0, 0), y1, y1)
    rx, ry = Symbol('rx'), Symbol('ry')
    for ind in range(0, 5):
        r = e3.random_point()
        # substitution should give zero*y1**2
        assert e3.equation(rx, ry).subs(zip((rx, ry), r.args)).equals(0)
    # test for the case with seed
    r = e3.random_point(seed=1)
    assert e3.equation(rx, ry).subs(zip((rx, ry), r.args)).equals(0)

