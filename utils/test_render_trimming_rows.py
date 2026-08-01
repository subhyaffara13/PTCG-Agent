
def test_render_trimming_rows(option, val):
    # test auto and specific trimming of rows
    df = DataFrame(np.arange(120).reshape(60, 2))
    with option_context(option, val):
        ctx = df.style._translate(True, True)
    assert len(ctx["head"][0]) == 3  # index + 2 data cols
    assert len(ctx["body"]) == 4  # 3 data rows + trimming row
    assert len(ctx["body"][0]) == 3  # index + 2 data cols

