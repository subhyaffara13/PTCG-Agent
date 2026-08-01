
def test_background_gradient_gmap_wrong_series(styler_blank):
    # test giving a gmap in Series form but with wrong axis
    msg = "'gmap' is a Series but underlying data for operations is a DataFrame"
    gmap = Series([1, 2], index=["X", "Y"])
    with pytest.raises(ValueError, match=msg):
        styler_blank.background_gradient(gmap=gmap, axis=None)._compute()

