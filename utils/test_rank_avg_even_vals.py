
def test_rank_avg_even_vals(dtype, upper):
    if upper:
        # use IntegerDtype/FloatingDtype
        dtype = dtype[0].upper() + dtype[1:]
        dtype = dtype.replace("Ui", "UI")
    df = DataFrame({"key": ["a"] * 4, "val": [1] * 4})
    df["val"] = df["val"].astype(dtype)
    assert df["val"].dtype == dtype

    result = df.groupby("key").rank()
    exp_df = DataFrame([2.5, 2.5, 2.5, 2.5], columns=["val"])
    if upper:
        exp_df = exp_df.astype("Float64")
    tm.assert_frame_equal(result, exp_df)

