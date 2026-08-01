
def test_issue_15947():
    assert f._diff_wrt is False
    raises(TypeError, lambda: f(f))
    raises(TypeError, lambda: f(x).diff(f))

