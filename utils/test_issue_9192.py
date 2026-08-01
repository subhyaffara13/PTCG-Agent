
def test_issue_9192():
    assert O(1)*O(1) == O(1)
    assert O(1)**O(1) == O(1)

