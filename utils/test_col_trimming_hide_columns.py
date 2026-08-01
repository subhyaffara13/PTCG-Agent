
def test_col_trimming_hide_columns():
    # gh 44272
    df = DataFrame([[1, 2, 3, 4, 5]])
    with option_context("styler.render.max_columns", 2):
        ctx = df.style.hide([0, 1], axis="columns")._translate(True, True)

    assert len(ctx["head"][0]) == 6  # blank, [0, 1 (hidden)], [2 ,3 (visible)], + trim
    for c, vals in enumerate([(1, False), (2, True), (3, True), ("...", True)]):
        assert ctx["head"][0][c + 2]["value"] == vals[0]
        assert ctx["head"][0][c + 2]["is_visible"] == vals[1]

    assert len(ctx["body"][0]) == 6  # index + 2 hidden + 2 visible + trimming col

