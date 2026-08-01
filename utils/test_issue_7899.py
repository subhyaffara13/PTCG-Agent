
def test_issue_7899():
    x = Symbol('x', real=True)
    assert (I*x).is_real is None
    assert ((x - I)*(x - 1)).is_zero is None
    assert ((x - I)*(x - 1)).is_real is None

