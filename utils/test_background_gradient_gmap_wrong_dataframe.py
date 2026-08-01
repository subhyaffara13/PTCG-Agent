
def test_background_gradient_gmap_wrong_dataframe(styler_blank, axis):
    # test giving a gmap in DataFrame but with wrong axis
    gmap = DataFrame([[1, 2], [2, 1]], columns=["A", "B"], index=["X", "Y"])
    msg = "'gmap' is a DataFrame but underlying data for operations is a Series"
    with pytest.raises(ValueError, match=msg):
        styler_blank.background_gradient(gmap=gmap, axis=axis)._compute()

