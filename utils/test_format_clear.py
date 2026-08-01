
def test_format_clear(styler, func, attr, kwargs):
    assert (0, 0) not in getattr(styler, attr)  # using default
    getattr(styler, func)("{:.2f}", **kwargs)
    assert (0, 0) in getattr(styler, attr)  # formatter is specified
    getattr(styler, func)(**kwargs)
    assert (0, 0) not in getattr(styler, attr)  # formatter cleared to default

