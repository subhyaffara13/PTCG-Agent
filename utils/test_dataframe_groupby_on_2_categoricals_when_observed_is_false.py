
def test_dataframe_groupby_on_2_categoricals_when_observed_is_false(
    reduction_func, observed, using_python_scalars
):
    # GH 23865
    # GH 27075
    # Ensure that df.groupby, when 'by' is two Categorical variables,
    # returns the categories that are not in df when observed=False/None

    if reduction_func == "ngroup":
        pytest.skip("ngroup does not return the Categories on the index")

    df = DataFrame(
        {
            "cat_1": Categorical(list("AABB"), categories=list("ABC")),
            "cat_2": Categorical(list("1111"), categories=list("12")),
            "value": [0.1, 0.1, 0.1, 0.1],
        }
    )
    unobserved_cats = [("A", "2"), ("B", "2"), ("C", "1"), ("C", "2")]

    df_grp = df.groupby(["cat_1", "cat_2"], observed=observed)

    args = get_groupby_method_args(reduction_func, df)

    if not observed and reduction_func in ["idxmin", "idxmax"]:
        # idxmin and idxmax are designed to fail on empty inputs
        with pytest.raises(
            ValueError, match="empty group due to unobserved categories"
        ):
            getattr(df_grp, reduction_func)(*args)
        return

    if reduction_func == "corrwith":
        warn = Pandas4Warning
        warn_msg = "DataFrameGroupBy.corrwith is deprecated"
    else:
        warn = None
        warn_msg = ""
    with tm.assert_produces_warning(warn, match=warn_msg):
        res = getattr(df_grp, reduction_func)(*args)

    expected = _results_for_groupbys_with_missing_categories[reduction_func]

    if using_python_scalars and reduction_func == "size":
        assert (res.loc[unobserved_cats] == expected).all() is True
    elif expected is np.nan:
        assert res.loc[unobserved_cats].isnull().all().all()
    else:
        assert (res.loc[unobserved_cats] == expected).all().all()

