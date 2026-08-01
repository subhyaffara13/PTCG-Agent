
def test_category_order_apply(as_index, sort, observed, method, index_kind, ordered):
    # GH#48749
    if (method == "transform" and index_kind == "range") or (
        not as_index and index_kind != "range"
    ):
        pytest.skip("No categories in result, nothing to test")
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
    gb = df.groupby(keys, as_index=as_index, sort=sort, observed=observed)
    op_result = getattr(gb, method)(lambda x: x.sum(numeric_only=True))
    if (method == "transform" or not as_index) and index_kind == "range":
        result = op_result["a"].cat.categories
    else:
        result = op_result.index.get_level_values("a").categories
    expected = Index([1, 4, 3, 2])
    tm.assert_index_equal(result, expected)

    if index_kind == "multi":
        result = op_result.index.get_level_values("a2").categories
        tm.assert_index_equal(result, expected)

