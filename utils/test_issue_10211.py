
def test_issue_10211():
    from sympy.abc import h, w
    assert integrate((1/sqrt((y-x)**2 + h**2)**3), (x,0,w), (y,0,w)) == \
        2*sqrt(1 + w**2/h**2)/h - 2/h

