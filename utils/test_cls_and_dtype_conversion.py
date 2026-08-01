
def test_cls_and_dtype_conversion(simple_dtype):
    s = m.SimpleStruct()
    assert s.astuple() == (False, 0, 0.0, 0.0)
    assert m.SimpleStruct.fromtuple(s.astuple()).astuple() == s.astuple()

    s.uint_ = 2
    assert m.f_simple(s) == 20

    # Try as recarray of shape==(1,).
    s_recarray = np.array([(False, 2, 0.0, 0.0)], dtype=simple_dtype)
    # Show that this will work for vectorized case.
    np.testing.assert_array_equal(m.f_simple_vectorized(s_recarray), [20])

    # Show as a scalar that inherits from np.generic.
    s_scalar = s_recarray[0]
    assert isinstance(s_scalar, np.void)
    assert m.f_simple(s_scalar) == 20

    # Show that an *array* scalar (np.ndarray.shape == ()) does not convert.
    # More specifically, conversion to SimpleStruct is not implicit.
    s_recarray_scalar = s_recarray.reshape(())
    assert isinstance(s_recarray_scalar, np.ndarray)
    assert s_recarray_scalar.dtype == simple_dtype
    with pytest.raises(TypeError) as excinfo:
        m.f_simple(s_recarray_scalar)
    assert "incompatible function arguments" in str(excinfo.value)
    # Explicitly convert to m.SimpleStruct.
    assert m.f_simple(m.SimpleStruct.fromtuple(s_recarray_scalar.item())) == 20

    # Show that an array of dtype=object does *not* convert.
    s_array_object = np.array([s])
    assert s_array_object.dtype == object
    with pytest.raises(TypeError) as excinfo:
        m.f_simple_vectorized(s_array_object)
    assert "incompatible function arguments" in str(excinfo.value)
    # Explicitly convert to `np.array(..., dtype=simple_dtype)`
    s_array = np.array([s.astuple()], dtype=simple_dtype)
    np.testing.assert_array_equal(m.f_simple_vectorized(s_array), [20])

