
def test_issue_5939():
    a = Symbol('a')
    b = Symbol('b')
    assert sympify('''a+\nb''') == a + b

