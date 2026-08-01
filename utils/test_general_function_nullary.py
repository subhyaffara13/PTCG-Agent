
def test_general_function_nullary():
    nu = Function('nu')

    e = nu()
    edx = e.diff(x)
    edxdx = e.diff(x).diff(x)
    assert e == nu()
    assert edx != nu()
    assert edx == 0
    assert edxdx == 0

