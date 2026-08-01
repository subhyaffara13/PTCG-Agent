
def test_FracElement___neg__():
    F, x,y = field("x,y", QQ)

    f = (7*x - 9)/y
    g = (-7*x + 9)/y

    assert -f == g
    assert -g == f

