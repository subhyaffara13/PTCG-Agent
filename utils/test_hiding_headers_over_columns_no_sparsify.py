
def test_hiding_headers_over_columns_no_sparsify():
    # GH 43464
    midx = MultiIndex.from_product([[1, 2], ["a", "a", "b"]])
    df = DataFrame(9, columns=midx, index=[0])
    ctx = df.style._translate(False, False)
    for ix in [(0, 1), (0, 2), (1, 1), (1, 2)]:
        assert ctx["head"][ix[0]][ix[1]]["is_visible"] is True
    ctx = df.style.hide((1, "a"), axis="columns")._translate(False, False)
    for ix in [(0, 1), (0, 2), (1, 1), (1, 2)]:
        assert ctx["head"][ix[0]][ix[1]]["is_visible"] is False

