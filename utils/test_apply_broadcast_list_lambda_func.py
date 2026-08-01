
def test_apply_broadcast_list_lambda_func(int_frame_const_col):
    # preserve columns
    df = int_frame_const_col
    result = df.apply(lambda x: [1, 2, 3], axis=1, result_type="broadcast")
    tm.assert_frame_equal(result, df)

