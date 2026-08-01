
def test_frame_setitem_view_direct(multiindex_dataframe_random_data):
    # this works because we are modifying the underlying array
    # really a no-no
    df = multiindex_dataframe_random_data.T
    with pytest.raises(ValueError, match="read-only"):
        df["foo"].values[:] = 0
    assert (df["foo"].values != 0).all()

