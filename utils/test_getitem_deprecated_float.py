
def test_getitem_deprecated_float(idx):
    # https://github.com/pandas-dev/pandas/issues/34191
    idx = Index(idx)
    msg = "Indexing with a float is no longer supported"
    with pytest.raises(IndexError, match=msg):
        idx[1.0]

