
def test_with_dictlike_columns_with_infer():
    # GH 17602
    df = DataFrame([[1, 2], [1, 2]], columns=["a", "b"])
    result = df.apply(lambda x: {"s": x["a"] + x["b"]}, axis=1, result_type="expand")
    expected = DataFrame({"s": [3, 3]})
    tm.assert_frame_equal(result, expected)

    df["tm"] = [
        Timestamp("2017-05-01 00:00:00"),
        Timestamp("2017-05-02 00:00:00"),
    ]
    result = df.apply(lambda x: {"s": x["a"] + x["b"]}, axis=1, result_type="expand")
    tm.assert_frame_equal(result, expected)

