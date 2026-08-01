
def test_numpy_int_convert():
    np = pytest.importorskip("numpy")

    convert, noconvert = m.int_passthrough, m.int_passthrough_noconvert

    def require_implicit(v):
        pytest.raises(TypeError, noconvert, v)

    # `np.intc` is an alias that corresponds to a C++ `int`
    assert convert(np.intc(42)) == 42
    assert noconvert(np.intc(42)) == 42

    # The implicit conversion from np.float32 is undesirable but currently accepted.
    # TODO: Avoid DeprecationWarning in `PyLong_AsLong` (and similar)
    # TODO: PyPy 3.8 does not behave like CPython 3.8 here yet (7.3.7)
    # https://github.com/pybind/pybind11/issues/3408
    if (3, 8) <= sys.version_info < (3, 10) and env.CPYTHON:
        with env.deprecated_call():
            assert convert(np.float32(3.14159)) == 3
    else:
        assert convert(np.float32(3.14159)) == 3
    require_implicit(np.float32(3.14159))

