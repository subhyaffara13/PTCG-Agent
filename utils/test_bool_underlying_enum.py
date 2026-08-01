
def test_bool_underlying_enum():
    assert type(m.ScopedBoolEnum.TRUE.__int__()) is int
    assert int(m.ScopedBoolEnum.FALSE) == 0
    assert hash(m.ScopedBoolEnum.TRUE) == 1
    assert type(m.ScopedBoolEnum.TRUE.__getstate__()) is int
    assert m.ScopedBoolEnum(1) == m.ScopedBoolEnum.TRUE
    # Enum could construct with a bool
    # (bool is a strict subclass of int, and False will be converted to 0)
    assert m.ScopedBoolEnum(False) == m.ScopedBoolEnum.FALSE

