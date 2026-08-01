
def test_trig_split():
    assert trig_split(cos(x), cos(y)) == (1, 1, 1, x, y, True)
    assert trig_split(2*cos(x), -2*cos(y)) == (2, 1, -1, x, y, True)
    assert trig_split(cos(x)*sin(y), cos(y)*sin(y)) == \
        (sin(y), 1, 1, x, y, True)

    assert trig_split(cos(x), -sqrt(3)*sin(x), two=True) == \
        (2, 1, -1, x, pi/6, False)
    assert trig_split(cos(x), sin(x), two=True) == \
        (sqrt(2), 1, 1, x, pi/4, False)
    assert trig_split(cos(x), -sin(x), two=True) == \
        (sqrt(2), 1, -1, x, pi/4, False)
    assert trig_split(sqrt(2)*cos(x), -sqrt(6)*sin(x), two=True) == \
        (2*sqrt(2), 1, -1, x, pi/6, False)
    assert trig_split(-sqrt(6)*cos(x), -sqrt(2)*sin(x), two=True) == \
        (-2*sqrt(2), 1, 1, x, pi/3, False)
    assert trig_split(cos(x)/sqrt(6), sin(x)/sqrt(2), two=True) == \
        (sqrt(6)/3, 1, 1, x, pi/6, False)
    assert trig_split(-sqrt(6)*cos(x)*sin(y),
            -sqrt(2)*sin(x)*sin(y), two=True) == \
        (-2*sqrt(2)*sin(y), 1, 1, x, pi/3, False)

    assert trig_split(cos(x), sin(x)) is None
    assert trig_split(cos(x), sin(z)) is None
    assert trig_split(2*cos(x), -sin(x)) is None
    assert trig_split(cos(x), -sqrt(3)*sin(x)) is None
    assert trig_split(cos(x)*cos(y), sin(x)*sin(z)) is None
    assert trig_split(cos(x)*cos(y), sin(x)*sin(y)) is None
    assert trig_split(-sqrt(6)*cos(x), sqrt(2)*sin(x)*sin(y), two=True) is \
        None

    assert trig_split(sqrt(3)*sqrt(x), cos(3), two=True) is None
    assert trig_split(sqrt(3)*root(x, 3), sin(3)*cos(2), two=True) is None
    assert trig_split(cos(5)*cos(6), cos(7)*sin(5), two=True) is None

