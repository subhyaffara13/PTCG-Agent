
def test_issue_12533():
    d = IndexedBase('d')
    assert IndexedBase(range(5)) == Range(0, 5, 1)
    assert d[0].subs(Symbol("d"), range(5)) == 0
    assert d[0].subs(d, range(5)) == 0
    assert d[1].subs(d, range(5)) == 1
    assert Indexed(Range(5), 2) == 2

