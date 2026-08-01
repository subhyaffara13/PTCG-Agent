
def test_closing_angle():
    a = Ray((0, 0), angle=0)
    b = Ray((1, 2), angle=pi/2)
    assert a.closing_angle(b) == -pi/2
    assert b.closing_angle(a) == pi/2
    assert a.closing_angle(a) == 0

