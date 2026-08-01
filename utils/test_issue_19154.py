
def test_issue_19154():
    assert limit(besseli(1, 3 *x)/(x *besseli(1, x)**3), x , oo) == 2*sqrt(3)*pi/3
    assert limit(besseli(1, 3 *x)/(x *besseli(1, x)**3), x , -oo) == -2*sqrt(3)*pi/3

