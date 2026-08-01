
def test_frame_setitem_copy_raises(multiindex_dataframe_random_data):
    # will raise/warn as its chained assignment
    df = multiindex_dataframe_random_data.T
    with tm.raises_chained_assignment_error():
        df["foo"]["one"] = 2

