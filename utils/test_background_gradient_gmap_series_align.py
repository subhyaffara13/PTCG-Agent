
def test_background_gradient_gmap_series_align(styler_blank, gmap, axis, exp_gmap):
    # test gmap given as Series that it aligns to the data including subset
    expected = styler_blank.background_gradient(axis=None, gmap=exp_gmap)._compute()
    result = styler_blank.background_gradient(axis=axis, gmap=gmap)._compute()
    assert expected.ctx == result.ctx

