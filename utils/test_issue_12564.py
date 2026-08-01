
def test_issue_12564():
    assert limit(x**2 + x*sin(x) + cos(x), x, -oo) is oo
    assert limit(x**2 + x*sin(x) + cos(x), x, oo) is oo
    assert limit(((x + cos(x))**2).expand(), x, oo) is oo
    assert limit(((x + sin(x))**2).expand(), x, oo) is oo
    assert limit(((x + cos(x))**2).expand(), x, -oo) is oo
    assert limit(((x + sin(x))**2).expand(), x, -oo) is oo

