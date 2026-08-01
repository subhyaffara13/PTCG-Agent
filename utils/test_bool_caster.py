
def test_bool_caster():
    """Test bool caster implicit conversions."""
    convert, noconvert = m.bool_passthrough, m.bool_passthrough_noconvert

    def require_implicit(v):
        pytest.raises(TypeError, noconvert, v)

    def cant_convert(v):
        pytest.raises(TypeError, convert, v)

    # straight up bool
    assert convert(True) is True
    assert convert(False) is False
    assert noconvert(True) is True
    assert noconvert(False) is False

    # None requires implicit conversion
    require_implicit(None)
    assert convert(None) is False

    class A:
        def __init__(self, x):
            self.x = x

        def __nonzero__(self):
            return self.x

        def __bool__(self):
            return self.x

    class B:
        pass

    # Arbitrary objects are not accepted
    cant_convert(object())
    cant_convert(B())

    # Objects with __nonzero__ / __bool__ defined can be converted
    require_implicit(A(True))
    assert convert(A(True)) is True
    assert convert(A(False)) is False

