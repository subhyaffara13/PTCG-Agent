
def test_align_axis(align, exp, axis):
    # test all axis combinations with positive values and different aligns
    data = DataFrame([[1, 2], [3, 4]])
    result = (
        data.style.bar(align=align, axis=None if axis == "none" else axis)
        ._compute()
        .ctx
    )
    expected = {
        (0, 0): exp[axis][0][0],
        (0, 1): exp[axis][0][1],
        (1, 0): exp[axis][1][0],
        (1, 1): exp[axis][1][1],
    }
    assert result == expected

