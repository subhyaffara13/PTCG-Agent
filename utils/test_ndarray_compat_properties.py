
def test_ndarray_compat_properties(index_or_series_obj):
    obj = index_or_series_obj

    # Check that we work.
    for p in ["shape", "dtype", "T", "nbytes"]:
        assert getattr(obj, p, None) is not None

    # deprecated properties
    for p in ["strides", "itemsize", "base", "data"]:
        assert not hasattr(obj, p)

    msg = "can only convert an array of size 1 to a Python scalar"
    with pytest.raises(ValueError, match=msg):
        obj.item()  # len > 1

    assert obj.ndim == 1
    assert obj.size == len(obj)

    assert Index([1]).item() == 1
    assert Series([1]).item() == 1


def test_ndarray_compat_properties(index):
    if isinstance(index, PeriodIndex) and not IS64:
        pytest.skip("Overflow")
    idx = index
    assert idx.T.equals(idx)
    assert idx.transpose().equals(idx)

    values = idx.values

    assert idx.shape == values.shape
    assert idx.ndim == values.ndim
    assert idx.size == values.size

    if not isinstance(index, (RangeIndex, MultiIndex)):
        # These two are not backed by an ndarray
        assert idx.nbytes == values.nbytes

    # test for validity
    idx.nbytes
    idx.values.nbytes

