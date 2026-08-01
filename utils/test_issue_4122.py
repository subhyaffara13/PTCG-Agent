
def test_issue_4122():
    x = Symbol('x', nonpositive=True)
    assert oo + x is oo
    x = Symbol('x', extended_nonpositive=True)
    assert (oo + x).is_Add
    x = Symbol('x', finite=True)
    assert (oo + x).is_Add  # x could be imaginary
    x = Symbol('x', nonnegative=True)
    assert oo + x is oo
    x = Symbol('x', extended_nonnegative=True)
    assert oo + x is oo
    x = Symbol('x', finite=True, real=True)
    assert oo + x is oo

    # similarly for negative infinity
    x = Symbol('x', nonnegative=True)
    assert -oo + x is -oo
    x = Symbol('x', extended_nonnegative=True)
    assert (-oo + x).is_Add
    x = Symbol('x', finite=True)
    assert (-oo + x).is_Add
    x = Symbol('x', nonpositive=True)
    assert -oo + x is -oo
    x = Symbol('x', extended_nonpositive=True)
    assert -oo + x is -oo
    x = Symbol('x', finite=True, real=True)
    assert -oo + x is -oo

