
def test_issue_14238():
    # doesn't cause recursion error
    r = Symbol('r', real=True)
    assert Abs(r + Piecewise((0, r > 0), (1 - r, True)))

