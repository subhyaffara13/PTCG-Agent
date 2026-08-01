
def test_length_nonmasked_marray_iterable_axis_raises():
    xp = marray._get_namespace(np)

    data = [[1.0, 2.0], [3.0, 4.0]]
    mask = [[False, False], [True, False]]
    marr = xp.asarray(data, mask=mask)

    # Axis tuples are not currently supported for MArray input.
    # This test can be removed after support is added.
    with pytest.raises(NotImplementedError,
        match="`axis` must be an integer or None for use with `MArray`"):
        _count_nonmasked(marr, axis=(0, 1), xp=xp)

