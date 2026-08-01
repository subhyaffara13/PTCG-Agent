
def test_background_gradient_gmap_array(styler_blank, axis, gmap, expected):
    # tests when gmap is given as a sequence and converted to ndarray
    result = styler_blank.background_gradient(axis=axis, gmap=gmap)._compute().ctx
    assert result == expected

