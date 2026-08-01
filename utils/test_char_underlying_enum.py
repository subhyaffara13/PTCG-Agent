
def test_char_underlying_enum():  # Issue #1331/PR #1334:
    assert type(m.ScopedCharEnum.Positive.__int__()) is int
    assert int(m.ScopedChar16Enum.Zero) == 0
    assert hash(m.ScopedChar32Enum.Positive) == 1
    assert type(m.ScopedCharEnum.Positive.__getstate__()) is int
    assert m.ScopedWCharEnum(1) == m.ScopedWCharEnum.Positive
    with pytest.raises(TypeError):
        # Even if the underlying type is char, only an int can be used to construct the enum:
        m.ScopedCharEnum("0")

