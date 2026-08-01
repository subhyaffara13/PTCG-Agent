
def test_subs_issue_4009():
    assert (I*Symbol('a')).subs(1, 2) == I*Symbol('a')

