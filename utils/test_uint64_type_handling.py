
def test_uint64_type_handling(dtype, how):
    # GH 26310
    df = DataFrame({"x": 6903052872240755750, "y": [1, 2]})
    expected = df.groupby("y").agg({"x": how})
    df.x = df.x.astype(dtype)
    result = df.groupby("y").agg({"x": how})
    if how not in ("mean", "median"):
        # mean and median always result in floats
        result.x = result.x.astype(np.int64)
    tm.assert_frame_equal(result, expected, check_exact=True)

