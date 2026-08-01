
def test_issue_8635_18176():
    x = Symbol('x', real=True)
    k = Symbol('k', positive=True)
    assert limit(x**n - x**(n - 0), x, oo) == 0
    assert limit(x**n - x**(n - 5), x, oo) == oo
    assert limit(x**n - x**(n - 2.5), x, oo) == oo
    assert limit(x**n - x**(n - k - 1), x, oo) == oo
    x = Symbol('x', positive=True)
    assert limit(x**n - x**(n - 1), x, oo) == oo
    assert limit(x**n - x**(n + 2), x, oo) == -oo

