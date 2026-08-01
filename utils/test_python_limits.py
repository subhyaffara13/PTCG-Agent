
def test_python_limits():
    assert python(limit(x, x, oo)) == 'e = oo'
    assert python(limit(x**2, x, 0)) == 'e = 0'

