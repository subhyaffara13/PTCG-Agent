
def test_issue_12092():
    f = implemented_function('f', lambda x: x**2)
    assert f(f(2)).evalf() == Float(16)

