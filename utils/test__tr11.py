
def test__TR11():

    assert _TR11(sin(x/3)*sin(2*x)*sin(x/4)/(cos(x/6)*cos(x/8))) == \
        4*sin(x/8)*sin(x/6)*sin(2*x),_TR11(sin(x/3)*sin(2*x)*sin(x/4)/(cos(x/6)*cos(x/8)))
    assert _TR11(sin(x/3)/cos(x/6)) == 2*sin(x/6)

    assert _TR11(cos(x/6)/sin(x/3)) == 1/(2*sin(x/6))
    assert _TR11(sin(2*x)*cos(x/8)/sin(x/4)) == sin(2*x)/(2*sin(x/8)), _TR11(sin(2*x)*cos(x/8)/sin(x/4))
    assert _TR11(sin(x)/sin(x/2)) == 2*cos(x/2)

