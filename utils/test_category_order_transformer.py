
def test_category_order_transformer(
    as_index, sort, observed, transformation_func, index_kind, ordered
):
    # GH#48749
    df = DataFrame(
        {
            "a": Categorical([2, 1, 2, 3], categories=[1, 4, 3, 2], ordered=ordered),
            "b": range(4),
        }
    )
    if index_kind == "single":
        keys = ["a"]
        df = df.set_index(keys)
    elif index_kind == "multi":
        keys = ["a", "a2"]
        df["a2"] = df["a"]
        df = df.set_index(keys)
    args = get_groupby_method_args(transformation_func, df)
    gb = df.groupby(keys, as_index=as_index, sort=sort, observed=observed)
    op_result = getattr(gb, transformation_func)(*args)
    result = op_result.index.get_level_values("a").categories
    expected = Index([1, 4, 3, 2])
    tm.assert_index_equal(result, expected)

    if index_kind == "multi":
        result = op_result.index.get_level_values("a2").categories
        tm.assert_index_equal(result, expected)

