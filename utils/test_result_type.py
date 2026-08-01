
def test_result_type(int_frame_const_col):
    # result_type should be consistent no matter which
    # path we take in the code
    df = int_frame_const_col

    result = df.apply(lambda x: [1, 2, 3], axis=1, result_type="expand")
    expected = df.copy()
    expected.columns = range(3)
    tm.assert_frame_equal(result, expected)

