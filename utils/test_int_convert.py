import sys

def test_int_convert():
    class Int:
        def __int__(self):
            return 42

    class NotInt:
        pass

    class Float:
        def __float__(self):
            return 41.99999

    class Index:
        def __index__(self):
            return 42

    class IntAndIndex:
        def __int__(self):
            return 42

        def __index__(self):
            return 0

    class RaisingTypeErrorOnIndex:
        def __index__(self):
            raise TypeError

        def __int__(self):
            return 42

    class RaisingValueErrorOnIndex:
        def __index__(self):
            raise ValueError

        def __int__(self):
            return 42

    convert, noconvert = m.int_passthrough, m.int_passthrough_noconvert

    def requires_conversion(v):
        pytest.raises(TypeError, noconvert, v)

    def cant_convert(v):
        pytest.raises(TypeError, convert, v)

    assert convert(7) == 7
    assert noconvert(7) == 7
    cant_convert(3.14159)
    # TODO: Avoid DeprecationWarning in `PyLong_AsLong` (and similar)
    # TODO: PyPy 3.8 does not behave like CPython 3.8 here yet (7.3.7)
    if (3, 8) <= sys.version_info < (3, 10) and env.CPYTHON:
        with env.deprecated_call():
            assert convert(Int()) == 42
    else:
        assert convert(Int()) == 42
    requires_conversion(Int())
    cant_convert(NotInt())
    cant_convert(Float())

    # Before Python 3.8, `PyLong_AsLong` does not pick up on `obj.__index__`,
    # but pybind11 "backports" this behavior.
    assert convert(Index()) == 42
    assert noconvert(Index()) == 42
    assert convert(IntAndIndex()) == 0  # Fishy; `int(DoubleThought)` == 42
    assert noconvert(IntAndIndex()) == 0
    assert convert(RaisingTypeErrorOnIndex()) == 42
    requires_conversion(RaisingTypeErrorOnIndex())
    assert convert(RaisingValueErrorOnIndex()) == 42
    requires_conversion(RaisingValueErrorOnIndex())

