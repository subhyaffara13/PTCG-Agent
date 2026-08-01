
def test_issue_4279():
    a, b = symbols('a b')
    assert O(a, a, b) + O(1, a, b) == O(1, a, b)
    assert O(b, a, b) + O(1, a, b) == O(1, a, b)
    assert O(a + b, a, b) + O(1, a, b) == O(1, a, b)
    assert O(1, a, b) + O(a, a, b) == O(1, a, b)
    assert O(1, a, b) + O(b, a, b) == O(1, a, b)
    assert O(1, a, b) + O(a + b, a, b) == O(1, a, b)

