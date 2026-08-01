
def test_rolling_wrong_param_min_period():
    # GH34037
    name_l = ["Alice"] * 5 + ["Bob"] * 5
    val_l = [np.nan, np.nan, 1, 2, 3, np.nan, 1, 2, 3, 4]
    test_df = DataFrame([name_l, val_l]).T
    test_df.columns = ["name", "val"]

    result_error_msg = (
        r"^[a-zA-Z._]*\(\) got an unexpected keyword argument 'min_period'"
    )
    with pytest.raises(TypeError, match=result_error_msg):
        test_df.groupby("name")["val"].rolling(window=2, min_period=1).sum()

