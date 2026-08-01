
def test_concise_formatter_exceptions(kwarg):
    locator = mdates.AutoDateLocator()
    kwargs = {kwarg: ['', '%Y']}
    match = f"{kwarg} argument must be a list"
    with pytest.raises(ValueError, match=match):
        mdates.ConciseDateFormatter(locator, **kwargs)

