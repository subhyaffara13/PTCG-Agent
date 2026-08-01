
def test_highlight_between_inclusive(styler, inclusive, expected):
    kwargs = {"left": 0, "right": 1, "subset": IndexSlice[[0, 1], :]}
    result = styler.highlight_between(**kwargs, inclusive=inclusive)._compute()
    assert result.ctx == expected

