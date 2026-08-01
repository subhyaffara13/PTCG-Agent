
def test_index_dtype(dtype):
    # We use subtraction in the indexing, so need to verify that uint8 works
    cm = mpl.colormaps["viridis"]
    assert_array_equal(cm(dtype(0)), cm(0))

