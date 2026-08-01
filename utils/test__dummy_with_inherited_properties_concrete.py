
def test__dummy_with_inherited_properties_concrete():
    x = Symbol('x')

    from sympy.core.containers import Tuple
    d = _dummy_with_inherited_properties_concrete(Tuple(x, 0, 5))
    assert d.is_real
    assert d.is_integer
    assert d.is_nonnegative
    assert d.is_extended_nonnegative

    d = _dummy_with_inherited_properties_concrete(Tuple(x, 1, 9))
    assert d.is_real
    assert d.is_integer
    assert d.is_positive
    assert d.is_odd is None

    d = _dummy_with_inherited_properties_concrete(Tuple(x, -5, 5))
    assert d.is_real
    assert d.is_integer
    assert d.is_positive is None
    assert d.is_extended_nonnegative is None
    assert d.is_odd is None

    d = _dummy_with_inherited_properties_concrete(Tuple(x, -1.5, 1.5))
    assert d.is_real
    assert d.is_integer is None
    assert d.is_positive is None
    assert d.is_extended_nonnegative is None

    N = Symbol('N', integer=True, positive=True)
    d = _dummy_with_inherited_properties_concrete(Tuple(x, 2, N))
    assert d.is_real
    assert d.is_positive
    assert d.is_integer

    # Return None if no assumptions are added
    N = Symbol('N', integer=True, positive=True)
    d = _dummy_with_inherited_properties_concrete(Tuple(N, 2, 4))
    assert d is None

    x = Symbol('x', negative=True)
    raises(InconsistentAssumptions,
           lambda: _dummy_with_inherited_properties_concrete(Tuple(x, 1, 5)))

