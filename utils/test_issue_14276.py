
def test_issue_14276():
    assert isinstance(limit(sin(x)**log(x), x, oo), Limit)
    assert isinstance(limit(sin(x)**cos(x), x, oo), Limit)
    assert isinstance(limit(sin(log(cos(x))), x, oo), Limit)
    assert limit((1 + 1/(x**2 + cos(x)))**(x**2 + x), x, oo) == E

