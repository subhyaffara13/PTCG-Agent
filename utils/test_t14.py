
def test_T14():
    x = symbols('x', real=True)
    assert limit(atan(-log(x)), x, 0, dir='+') == pi/2

