
def test_merge_right_on_and_right_index():
    df1 = DataFrame({"col": [1, 2, 3]})
    df2 = DataFrame({"col": [2, 3, 4]})

    with pytest.raises(pd.errors.MergeError):
        df1.merge(df2, left_on="col", right_on="col", right_index=True)

