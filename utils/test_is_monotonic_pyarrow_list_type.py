
def test_is_monotonic_pyarrow_list_type():
    # GH 57333
    import pyarrow as pa

    idx = Index([[1], [2, 3]], dtype=pd.ArrowDtype(pa.list_(pa.int64())))
    assert not idx.is_monotonic_increasing
    assert not idx.is_monotonic_decreasing

