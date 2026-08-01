
def test_category_order_reducer(
    request, as_index, sort, observed, reduction_func, index_kind, ordered
):
    # GH#48749
    if reduction_func == "corrwith" and not as_index and index_kind != "single":
        msg = "GH#49950 - corrwith with as_index=False may not have grouping column"
        request.applymarker(pytest.mark.xfail(reason=msg))
    elif index_kind != "range" and not as_index:
        pytest.skip(reason="Result doesn't have categories, nothing to test")
    df = DataFrame(
        {
            "a": Categorical([2, 1, 2, 3], categories=[1, 4, 3, 2], ordered=ordered),
            "b": range(4),
        }
    )
    if index_kind == "range":
        keys = ["a"]
    elif index_kind == "single":
        keys = ["a"]
        df = df.set_index(keys)
    elif index_kind == "multi":
        keys = ["a", "a2"]
        df["a2"] = df["a"]
        df = df.set_index(keys)
    args = get_groupby_method_args(reduction_func, df)
    gb = df.groupby(keys, as_index=as_index, sort=sort, observed=observed)

    if not observed and reduction_func in ["idxmin", "idxmax"]:
        # idxmin and idxmax are designed to fail on empty inputs
        with pytest.raises(
            ValueError, match="empty group due to unobserved categories"
        ):
            getattr(gb, reduction_func)(*args)
        return
    if reduction_func == "corrwith":
        warn = Pandas4Warning
        warn_msg = "DataFrameGroupBy.corrwith is deprecated"
    else:
        warn = None
        warn_msg = ""
    with tm.assert_produces_warning(warn, match=warn_msg):
        op_result = getattr(gb, reduction_func)(*args)
    if as_index:
        result = op_result.index.get_level_values("a").categories
    else:
        result = op_result["a"].cat.categories
    expected = Index([1, 4, 3, 2])
    tm.assert_index_equal(result, expected)

    if index_kind == "multi":
        result = op_result.index.get_level_values("a2").categories
        tm.assert_index_equal(result, expected)

