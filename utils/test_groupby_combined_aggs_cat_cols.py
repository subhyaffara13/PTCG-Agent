
def test_groupby_combined_aggs_cat_cols(grp_col_dict, exp_data):
    # test combined aggregations on ordered categorical cols GH27800

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

    # unpack the grp_col_dict to create the multi-index tuple
    # this tuple will be used to create the expected dataframe index
    multi_index_list = []
    for k, v in grp_col_dict.items():
        if isinstance(v, list):
            multi_index_list.extend([k, value] for value in v)
        else:
            multi_index_list.append([k, v])
    multi_index = MultiIndex.from_tuples(tuple(multi_index_list))

    expected_df = DataFrame(data=exp_data, columns=multi_index, index=cat_index)
    for col in expected_df.columns:
        if isinstance(col, tuple) and "cat_ord" in col:
            # ordered categorical should be preserved
            expected_df[col] = expected_df[col].astype(input_df["cat_ord"].dtype)

    tm.assert_frame_equal(result_df, expected_df)

