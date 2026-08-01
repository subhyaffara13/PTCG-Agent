
def test_rank_zero_div(input_key, input_value, output_value):
    # GH 23666
    df = DataFrame({"A": input_key, "B": input_value})

    result = df.groupby("A").rank(method="dense", pct=True)
    expected = DataFrame({"B": output_value})
    tm.assert_frame_equal(result, expected)

