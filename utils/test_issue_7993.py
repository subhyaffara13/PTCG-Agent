
def test_issue_7993():
    x = Dummy(integer=True)
    y = Dummy(noninteger=True)
    assert (x - y).is_zero is False

