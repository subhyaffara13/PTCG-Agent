
def test_render_trimming_cols(option, val):
    # test auto and specific trimming of cols
    df = DataFrame(np.arange(30).reshape(3, 10))
    with option_context(option, val):
        ctx = df.style._translate(True, True)
    assert len(ctx["head"][0]) == 4  # index + 2 data cols + trimming col
    assert len(ctx["body"]) == 3  # 3 data rows
    assert len(ctx["body"][0]) == 4  # index + 2 data cols + trimming col

