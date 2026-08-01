
def test_issue_11856():
    t = symbols('t')
    assert integrate(sinc(pi*t), t) == Si(pi*t)/pi

