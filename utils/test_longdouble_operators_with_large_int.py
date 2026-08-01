
def test_longdouble_operators_with_large_int(sctype, op):
    # (See `test_longdouble_operators_with_obj` for why longdouble is special)
    # NEP 50 means that the result is clearly a (c)longdouble here:
    if sctype == np.clongdouble and op in [operator.mod, operator.floordiv]:
        # The above operators are not support for complex though...
        with pytest.raises(TypeError):
            op(sctype(3), 2**64)
        with pytest.raises(TypeError):
            op(sctype(3), 2**64)
    else:
        assert op(sctype(3), -2**64) == op(sctype(3), sctype(-2**64))
        assert op(2**64, sctype(3)) == op(sctype(2**64), sctype(3))

