
def test_issue_3101():
    e = x - y
    a = str(e)
    b = str(e)
    assert a == b

