
def test_issue_17661():
    c1 = Cycle(1,2)
    c2 = Cycle(1,2)
    assert c1 == c2
    assert repr(c1) == 'Cycle(1, 2)'
    assert c1 == c2

