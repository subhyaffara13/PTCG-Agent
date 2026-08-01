
def test_clines_multiindex(clines, expected, env):
    # also tests simultaneously with hidden rows and a hidden multiindex level
    midx = MultiIndex.from_product([["A", "-", "B"], [0], ["X", "Y"]])
    df = DataFrame([[1], [2], [99], [99], [3], [4]], index=midx)
    styler = df.style
    styler.hide([("-", 0, "X"), ("-", 0, "Y")])
    styler.hide(level=1)
    result = styler.to_latex(clines=clines, environment=env)
    assert expected in result

