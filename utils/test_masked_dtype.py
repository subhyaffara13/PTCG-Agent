
def test_masked_dtype():
    # When _masked_arrays_2_sentinel_arrays was first added, it always
    # upcast the arrays to np.float64. After gh16662, check expected promotion
    # and that the expected sentinel is found.

    # these are important because the max of the promoted dtype is the first
    # candidate to be the sentinel value
    max16 = np.iinfo(np.int16).max
    max128c = np.finfo(np.complex128).max

    # a is a regular array, b has masked elements, and c has no masked elements
    a = np.array([1, 2, max16], dtype=np.int16)
    b = np.ma.array([1, 2, 1], dtype=np.int8, mask=[0, 1, 0])
    c = np.ma.array([1, 2, 1], dtype=np.complex128, mask=[0, 0, 0])

    # check integer masked -> sentinel conversion
    out_arrays, sentinel = _masked_arrays_2_sentinel_arrays([a, b])
    a_out, b_out = out_arrays
    assert sentinel == max16-1  # not max16 because max16 was in the data
    assert b_out.dtype == np.int16  # check expected promotion
    assert_allclose(b_out, [b[0], sentinel, b[-1]])  # check sentinel placement
    assert a_out is a  # not a masked array, so left untouched
    assert not isinstance(b_out, np.ma.MaskedArray)  # b became regular array

    # similarly with complex
    out_arrays, sentinel = _masked_arrays_2_sentinel_arrays([b, c])
    b_out, c_out = out_arrays
    assert sentinel == max128c  # max128c was not in the data
    assert b_out.dtype == np.complex128  # b got promoted
    assert_allclose(b_out, [b[0], sentinel, b[-1]])  # check sentinel placement
    assert not isinstance(b_out, np.ma.MaskedArray)  # b became regular array
    assert not isinstance(c_out, np.ma.MaskedArray)  # c became regular array

    # Also, check edge case when a sentinel value cannot be found in the data
    min8, max8 = np.iinfo(np.int8).min, np.iinfo(np.int8).max
    a = np.arange(min8, max8+1, dtype=np.int8)  # use all possible values
    mask1 = np.zeros_like(a, dtype=bool)
    mask0 = np.zeros_like(a, dtype=bool)

    # a masked value can be used as the sentinel
    mask1[1] = True
    a1 = np.ma.array(a, mask=mask1)
    out_arrays, sentinel = _masked_arrays_2_sentinel_arrays([a1])
    assert sentinel == min8+1

    # unless it's the smallest possible; skipped for simiplicity (see code)
    mask0[0] = True
    a0 = np.ma.array(a, mask=mask0)
    message = "This function replaces masked elements with sentinel..."
    with pytest.raises(ValueError, match=message):
        _masked_arrays_2_sentinel_arrays([a0])

    # test that dtype is preserved in functions
    a = np.ma.array([1, 2, 3], mask=[0, 1, 0], dtype=np.float32)
    assert stats.gmean(a).dtype == np.float32

