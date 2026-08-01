
def test_issue_3679():
    # definite integration of rational functions gives wrong answers
    assert NS(Integral(1/(x**2 - 8*x + 17), (x, 2, 4))) == '1.10714871779409'

