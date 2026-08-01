
def test_series_groupby_on_2_categoricals_unobserved_zeroes_or_nans(
    reduction_func, request
):
    # GH 17605
    # Tests whether the unobserved categories in the result contain 0 or NaN

    if reduction_func == "ngroup":
        pytest.skip("ngroup is not truly a reduction")

    if reduction_func == "corrwith":  # GH 32293
        mark = pytest.mark.xfail(
            reason="TODO: implemented SeriesGroupBy.corrwith. See GH 32293"
        )
        request.applymarker(mark)

    df = DataFrame(
        {
            "cat_1": Categorical(list("AABB"), categories=list("ABC")),
            "cat_2": Categorical(list("AB") * 2, categories=list("ABC")),
            "value": [0.1] * 4,
        }
    )
    unobserved = [tuple("AC"), tuple("BC"), tuple("CA"), tuple("CB"), tuple("CC")]
    args = get_groupby_method_args(reduction_func, df)

    series_groupby = df.groupby(["cat_1", "cat_2"], observed=False)["value"]
    agg = getattr(series_groupby, reduction_func)

    if reduction_func in ["idxmin", "idxmax"]:
        # idxmin and idxmax are designed to fail on empty inputs
        with pytest.raises(
            ValueError, match="empty group due to unobserved categories"
        ):
            agg(*args)
        return

    result = agg(*args)

    missing_fillin = _results_for_groupbys_with_missing_categories[reduction_func]

    for idx in unobserved:
        val = result.loc[idx]
        assert (pd.isna(missing_fillin) and pd.isna(val)) or (val == missing_fillin)

    # If we expect unobserved values to be zero, we also expect the dtype to be int.
    # Except for .sum(). If the observed categories sum to dtype=float (i.e. their
    # sums have decimals), then the zeros for the missing categories should also be
    # floats.
    if missing_fillin == 0:
        if reduction_func in ["count", "nunique", "size"]:
            assert np.issubdtype(result.dtype, np.integer)
        else:
            assert reduction_func in ["sum", "any"]

