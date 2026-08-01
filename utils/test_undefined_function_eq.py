
def test_undefined_function_eq():
    f = Function('f')
    f2 = Function('f')
    g = Function('g')
    f_real = Function('f', is_real=True)

    # This test may only be meaningful if the cache is turned off
    assert f == f2
    assert hash(f) == hash(f2)
    assert f == f

    assert f != g

    assert f != f_real

