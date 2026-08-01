
def test_NDimArray():
    assert sstr(NDimArray(1.0), full_prec=True) == '1.00000000000000'
    assert sstr(NDimArray(1.0), full_prec=False) == '1.0'
    assert sstr(NDimArray([1.0, 2.0]), full_prec=True) == '[1.00000000000000, 2.00000000000000]'
    assert sstr(NDimArray([1.0, 2.0]), full_prec=False) == '[1.0, 2.0]'
    assert sstr(NDimArray([], (0,))) == 'ImmutableDenseNDimArray([], (0,))'
    assert sstr(NDimArray([], (0, 0))) == 'ImmutableDenseNDimArray([], (0, 0))'
    assert sstr(NDimArray([], (0, 1))) == 'ImmutableDenseNDimArray([], (0, 1))'
    assert sstr(NDimArray([], (1, 0))) == 'ImmutableDenseNDimArray([], (1, 0))'

