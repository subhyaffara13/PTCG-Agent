
def test_issue_10829():
    assert (4**x).subs(2**x, y) == y**2
    assert (9**x).subs(3**x, y) == y**2

