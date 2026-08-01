
def test_issue_8653():
    n = Symbol('n', integer=True)
    assert sin(n).is_irrational is None
    assert cos(n).is_irrational is None
    assert tan(n).is_irrational is None

