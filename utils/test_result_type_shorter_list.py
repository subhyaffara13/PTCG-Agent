
def test_result_type_shorter_list(int_frame_const_col):
    # result_type should be consistent no matter which
    # path we take in the code
    df = int_frame_const_col
    result = df.apply(lambda x: [1, 2], axis=1, result_type="expand")
    expected = df[["A", "B"]].copy()
    expected.columns = range(2)
    tm.assert_frame_equal(result, expected)

