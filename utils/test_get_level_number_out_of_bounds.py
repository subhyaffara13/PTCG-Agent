
def test_get_level_number_out_of_bounds(multiindex_dataframe_random_data):
    frame = multiindex_dataframe_random_data

    with pytest.raises(IndexError, match="Too many levels"):
        frame.index._get_level_number(2)
    with pytest.raises(IndexError, match="not a valid level number"):
        frame.index._get_level_number(-3)

