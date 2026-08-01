
def test_function_comparable_infinities():
    assert sin(oo).is_comparable is False
    assert sin(-oo).is_comparable is False
    assert sin(zoo).is_comparable is False
    assert sin(nan).is_comparable is False

