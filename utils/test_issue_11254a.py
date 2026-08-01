
def test_issue_11254a():
    assert integrate(sech(x), (x, 0, 1)) == 2*atan(tanh(S.Half))

