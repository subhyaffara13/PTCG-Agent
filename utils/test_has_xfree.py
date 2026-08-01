
def test_has_xfree():
    assert (x + 1).has_xfree({x})
    assert ((x + 1)**2).has_xfree({x + 1})
    assert not (x + y + 1).has_xfree({x + 1})
    raises(TypeError, lambda: x.has_xfree(x))
    raises(TypeError, lambda: x.has_xfree([x]))

