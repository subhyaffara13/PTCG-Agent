
def test_render_trimming_mi():
    midx = MultiIndex.from_product([[1, 2], [1, 2, 3]])
    df = DataFrame(np.arange(36).reshape(6, 6), columns=midx, index=midx)
    with option_context("styler.render.max_elements", 4):
        ctx = df.style._translate(True, True)

    assert len(ctx["body"][0]) == 5  # 2 indexes + 2 data cols + trimming row
    assert {"attributes": 'rowspan="2"'}.items() <= ctx["body"][0][0].items()
    assert {"class": "data row0 col_trim"}.items() <= ctx["body"][0][4].items()
    assert {"class": "data row_trim col_trim"}.items() <= ctx["body"][2][4].items()
    assert len(ctx["body"]) == 3  # 2 data rows + trimming row

