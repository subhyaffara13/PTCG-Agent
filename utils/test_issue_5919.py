
def test_issue_5919():
    assert (x/(y*(1 + y))).expand() == x/(y**2 + y)

