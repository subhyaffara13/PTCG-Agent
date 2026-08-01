
def test_sympify_float():
    assert sympify("1e-64") != 0
    assert sympify("1e-20000") != 0

