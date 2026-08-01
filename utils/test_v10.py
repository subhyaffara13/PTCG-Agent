
def test_V10():
    assert integrate(1/(3 + 3*cos(x) + 4*sin(x)), x) == log(4*tan(x/2) + 3)/4

