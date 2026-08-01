
def test_issue_17858():
    assert 1 in Range(-oo, oo)
    assert 0 in Range(oo, -oo, -1)
    assert oo not in Range(-oo, oo)
    assert -oo not in Range(-oo, oo)

