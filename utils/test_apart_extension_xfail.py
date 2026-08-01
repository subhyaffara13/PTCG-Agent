
def test_apart_extension_xfail():
    f, g = _make_extension_example()
    assert apart(f, x, extension={sqrt(2)}) == g

