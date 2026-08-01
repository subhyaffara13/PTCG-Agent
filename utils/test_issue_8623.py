
def test_issue_8623():
    assert integrate((1 + cos(2*x)) / (3 - 2*cos(2*x)), (x, 0, pi)) == -pi/2 + sqrt(5)*pi/2
    assert integrate((1 + cos(2*x))/(3 - 2*cos(2*x))) == -x/2 + sqrt(5)*(atan(sqrt(5)*tan(x)) + \
        pi*floor((x - pi/2)/pi))/2

