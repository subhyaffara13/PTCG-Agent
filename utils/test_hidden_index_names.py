
def test_hidden_index_names(mi_df):
    mi_df.index.names = ["Lev0", "Lev1"]
    mi_styler = mi_df.style
    ctx = mi_styler._translate(True, True)
    assert len(ctx["head"]) == 3  # 2 column index levels + 1 index names row

    mi_styler.hide(axis="index", names=True)
    ctx = mi_styler._translate(True, True)
    assert len(ctx["head"]) == 2  # index names row is unparsed
    for i in range(4):
        assert ctx["body"][0][i]["is_visible"]  # 2 index levels + 2 data values visible

    mi_styler.hide(axis="index", level=1)
    ctx = mi_styler._translate(True, True)
    assert len(ctx["head"]) == 2  # index names row is still hidden
    assert ctx["body"][0][0]["is_visible"] is True
    assert ctx["body"][0][1]["is_visible"] is False

