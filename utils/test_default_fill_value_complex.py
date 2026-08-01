
def test_default_fill_value_complex():
    # regression test for Python 3, where 'unicode' was not defined
    assert_(default_fill_value(1 + 1j) == 1.e20 + 0.0j)

