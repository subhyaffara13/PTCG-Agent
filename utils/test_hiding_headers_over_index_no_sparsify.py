
def test_hiding_headers_over_index_no_sparsify():
    # GH 43464
    midx = MultiIndex.from_product([[1, 2], ["a", "a", "b"]])
    df = DataFrame(9, index=midx, columns=[0])
    ctx = df.style._translate(False, False)
    assert len(ctx["body"]) == 6
    ctx = df.style.hide((1, "a"), axis=0)._translate(False, False)
    assert len(ctx["body"]) == 4
    assert "row2" in ctx["body"][0][0]["class"]

