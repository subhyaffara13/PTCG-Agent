
def test_against_frame_and_seriesgroupby(
    education_df,
    groupby,
    normalize,
    name,
    sort,
    ascending,
    as_index,
    frame,
    request,
    using_infer_string,
):
    # test all parameters:
    # - Use column, array or function as by= parameter
    # - Whether or not to normalize
    # - Whether or not to sort and how
    # - Whether or not to use the groupby as an index
    # - 3-way compare against:
    #   - apply with :meth:`~DataFrame.value_counts`
    #   - `~SeriesGroupBy.value_counts`
    if frame and sort and normalize:
        request.applymarker(
            pytest.mark.xfail(
                reason=(
                    "pandas default unstable sorting of duplicates"
                    "issue with numpy>=1.25 with AVX instructions"
                ),
                strict=False,
            )
        )
    by = {
        "column": "country",
        "array": education_df["country"].values,
        "function": lambda x: education_df["country"][x] == "US",
    }[groupby]

    gp = education_df.groupby(by=by, as_index=as_index)
    result = gp[["gender", "education"]].value_counts(
        normalize=normalize, sort=sort, ascending=ascending
    )
    if frame:
        # compare against apply with DataFrame value_counts
        expected = gp.apply(
            _frame_value_counts, ["gender", "education"], normalize, sort, ascending
        )

        if as_index:
            tm.assert_series_equal(result, expected)
        else:
            name = "proportion" if normalize else "count"
            expected = expected.reset_index().rename({0: name}, axis=1)
            if groupby in ["array", "function"] and (not as_index and frame):
                expected.insert(loc=0, column="level_0", value=result["level_0"])
            else:
                expected.insert(loc=0, column="country", value=result["country"])
            tm.assert_frame_equal(result, expected)
    else:
        # compare against SeriesGroupBy value_counts
        education_df["both"] = education_df["gender"] + "-" + education_df["education"]
        expected = gp["both"].value_counts(
            normalize=normalize, sort=sort, ascending=ascending
        )
        expected.name = name
        if as_index:
            index_frame = expected.index.to_frame(index=False)
            index_frame["gender"] = index_frame["both"].str.split("-").str.get(0)
            index_frame["education"] = index_frame["both"].str.split("-").str.get(1)
            both_dtype = index_frame["both"].dtype
            index_frame = index_frame.astype(
                {"gender": both_dtype, "education": both_dtype}
            )
            del index_frame["both"]
            index_frame2 = index_frame.rename({0: None}, axis=1)
            expected.index = MultiIndex.from_frame(index_frame2)

            if index_frame2.columns.isna()[0]:
                # with using_infer_string, the columns in index_frame as string
                #  dtype, which makes the rename({0: None}) above use np.nan
                #  instead of None, so we need to set None more explicitly.
                expected.index.names = [None, *expected.index.names[1:]]
            tm.assert_series_equal(result, expected)
        else:
            expected.insert(1, "gender", expected["both"].str.split("-").str.get(0))
            expected.insert(2, "education", expected["both"].str.split("-").str.get(1))
            if using_infer_string:
                expected = expected.astype({"gender": "str", "education": "str"})
            del expected["both"]
            tm.assert_frame_equal(result, expected)

