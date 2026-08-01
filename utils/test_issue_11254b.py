
def test_issue_11254b():
    assert integrate(csch(x), x) == log(tanh(x/2))
    assert integrate(csch(x), (x, 0, 1)) == oo

