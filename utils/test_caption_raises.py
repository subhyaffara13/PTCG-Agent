
def test_caption_raises(mi_styler, caption):
    msg = "`caption` must be either a string or 2-tuple of strings."
    with pytest.raises(ValueError, match=msg):
        mi_styler.set_caption(caption)

