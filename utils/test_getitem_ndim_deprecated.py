
def test_getitem_ndim_deprecated(data):
    series = Series(data)
    with pytest.raises(ValueError, match="Multi-dimensional indexing"):
        series[:, None]

