
def test_Type__cast_check__integers():
    # Rounding
    raises(ValueError, lambda: integer.cast_check(3.5))
    assert integer.cast_check('3') == 3
    assert integer.cast_check(Float('3.0000000000000000000')) == 3
    assert integer.cast_check(Float('3.0000000000000000001')) == 3  # unintuitive maybe?

    # Range
    assert int8.cast_check(127.0) == 127
    raises(ValueError, lambda: int8.cast_check(128))
    assert int8.cast_check(-128) == -128
    raises(ValueError, lambda: int8.cast_check(-129))

    assert uint8.cast_check(0) == 0
    assert uint8.cast_check(128) == 128
    raises(ValueError, lambda: uint8.cast_check(256.0))
    raises(ValueError, lambda: uint8.cast_check(-1))

