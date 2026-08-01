
def test_issue_18400():
    n = Symbol('n', integer=True)
    raises(ValueError, lambda: imageset(lambda x: x*2, Range(n)))

    n = Symbol('n', integer=True, positive=True)
    # No exception
    assert imageset(lambda x: x*2, Range(n)) == imageset(lambda x: x*2, Range(n))

