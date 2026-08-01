
def test_frame_mi_empty_slice():
    # GH 15454
    df = DataFrame(0, index=range(2), columns=MultiIndex.from_product([[1], [2]]))
    result = df[[]]
    expected = DataFrame(
        index=[0, 1], columns=MultiIndex(levels=[[1], [2]], codes=[[], []])
    )
    tm.assert_frame_equal(result, expected)

