
def test_issue_17130():
    e = Add(b, -b, I, -I, evaluate=False)
    assert e.is_zero is None # ideally this would be True

