
def test_concat_ea_upcast():
    # GH#54848
    df1 = DataFrame(["a"], dtype="string")
    df2 = DataFrame([1], dtype="Int64")
    result = concat([df1, df2])
    expected = DataFrame(["a", 1], index=[0, 0])
    tm.assert_frame_equal(result, expected)

