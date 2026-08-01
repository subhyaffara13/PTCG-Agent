
def test_issue_6158():
    assert (x - 1).subs(1, y) == x - y
    assert (x - 1).subs(-1, y) == x + y
    assert (x - oo).subs(oo, y) == x - y
    assert (x - oo).subs(-oo, y) == x + y

