
def test_issue_21823():
    assert str(Partition([1, 2])) == 'Partition({1, 2})'
    assert str(Partition({1, 2})) == 'Partition({1, 2})'

