
def test_format_index_names_level(axis, level, expected):
    midx = MultiIndex.from_arrays([["_", "_"], ["_", "_"]], names=["zero", "one"])
    df = DataFrame([[1, 2], [3, 4]])
    if axis == 0:
        df.index = midx
    else:
        df.columns = midx

    styler = df.style.format_index_names(lambda v: "X", level=level, axis=axis)
    ctx = styler._translate(True, True)

    if axis == 0:  # compare index
        result = [ctx["head"][1][s]["display_value"] for s in range(2)]
    else:  # compare columns
        result = [ctx["head"][s][0]["display_value"] for s in range(2)]
    assert expected == result

