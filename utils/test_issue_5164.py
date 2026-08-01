
def test_issue_5164():
    assert limit(x**0.5, x, oo) == oo**0.5 is oo
    assert limit(x**0.5, x, 16) == 4 # Should this be a float?
    assert limit(x**0.5, x, 0) == 0
    assert limit(x**(-0.5), x, oo) == 0
    assert limit(x**(-0.5), x, 4) == S.Half # Should this be a float?

