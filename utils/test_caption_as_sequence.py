
def test_caption_as_sequence(styler):
    styler.set_caption(("full cap", "short cap"))
    assert "<caption>full cap</caption>" in styler.to_html()

