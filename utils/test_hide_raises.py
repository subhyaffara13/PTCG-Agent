
def test_hide_raises(mi_styler):
    msg = "`subset` and `level` cannot be passed simultaneously"
    with pytest.raises(ValueError, match=msg):
        mi_styler.hide(axis="index", subset="something", level="something else")

    msg = "`level` must be of type `int`, `str` or list of such"
    with pytest.raises(ValueError, match=msg):
        mi_styler.hide(axis="index", level={"bad": 1, "type": 2})

