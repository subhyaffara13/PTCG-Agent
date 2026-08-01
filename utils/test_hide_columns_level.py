
def test_hide_columns_level(mi_styler, level, names):
    mi_styler.columns.names = ["zero", "one"]
    if names:
        mi_styler.index.names = ["zero", "one"]
    ctx = mi_styler.hide(axis="columns", level=level)._translate(True, False)
    assert len(ctx["head"]) == (2 if names else 1)

