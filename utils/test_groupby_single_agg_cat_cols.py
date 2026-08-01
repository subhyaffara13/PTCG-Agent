
def test_groupby_single_agg_cat_cols(grp_col_dict, exp_data):
    # test single aggregations on ordered categorical cols GHGH27800

    # create the result dataframe
    input_df = DataFrame(
        {
            "nr": [1, 2, 3, 4, 5, 6, 7, 8],
            "cat_ord": list("aabbccdd"),
            "cat": list("aaaabbbb"),
        }
    )

    input_df = input_df.astype({"cat": "category", "cat_ord": "category"})
    input_df["cat_ord"] = input_df["cat_ord"].cat.as_ordered()
    result_df = input_df.groupby("cat", observed=False).agg(grp_col_dict)

    # create expected dataframe
    cat_index = pd.CategoricalIndex(
        ["a", "b"], categories=["a", "b"], ordered=False, name="cat", dtype="category"
    )

    expected_df = DataFrame(data=exp_data, index=cat_index)

    if "cat_ord" in expected_df:
        # ordered categorical columns should be preserved
        dtype = input_df["cat_ord"].dtype
        expected_df["cat_ord"] = expected_df["cat_ord"].astype(dtype)

    tm.assert_frame_equal(result_df, expected_df)

