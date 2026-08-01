
def test_unions():
    int_float_union = m.IntFloat()
    int_float_union.i = 42
    assert int_float_union.i == 42
    int_float_union.f = 3.0
    assert int_float_union.f == 3.0

