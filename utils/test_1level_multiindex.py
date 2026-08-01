
def test_1level_multiindex():
    # GH 43383
    midx = MultiIndex.from_product([[1, 2]], names=[""])
    df = DataFrame(-1, index=midx, columns=[0, 1])
    ctx = df.style._translate(True, True)
    assert ctx["body"][0][0]["display_value"] == "1"
    assert ctx["body"][0][0]["is_visible"] is True
    assert ctx["body"][1][0]["display_value"] == "2"
    assert ctx["body"][1][0]["is_visible"] is True

