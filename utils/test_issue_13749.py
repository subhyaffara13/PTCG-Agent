
def test_issue_13749():
    assert integrate(1 / (2 + cos(x)), (x, 0, pi)) == pi/sqrt(3)
    assert integrate(1/(2 + cos(x))) == 2*sqrt(3)*(atan(sqrt(3)*tan(x/2)/3) + pi*floor((x/2 - pi/2)/pi))/3

