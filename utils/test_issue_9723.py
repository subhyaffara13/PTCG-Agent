
def test_issue_9723():
    assert integrate(sqrt(x + sqrt(x))) == \
        2*sqrt(sqrt(x) + x)*(sqrt(x)/12 + x/3 - S(1)/8) + log(2*sqrt(x) + 2*sqrt(sqrt(x) + x) + 1)/8
    assert integrate(sqrt(2*x+3+sqrt(4*x+5))**3) == \
        sqrt(2*x + sqrt(4*x + 5) + 3) * \
           (9*x/10 + 11*(4*x + 5)**(S(3)/2)/40 + sqrt(4*x + 5)/40 + (4*x + 5)**2/10 + S(11)/10)/2

