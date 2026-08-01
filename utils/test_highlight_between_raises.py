
def test_highlight_between_raises(arg, styler, map, axis):
    msg = f"supplied '{arg}' is not correct shape"
    with pytest.raises(ValueError, match=msg):
        styler.highlight_between(**{arg: map, "axis": axis})._compute()

