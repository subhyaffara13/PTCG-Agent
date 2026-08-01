
def test_issue_6753():
    assert (1 + x**2)**10000*O(x) == O(x)

