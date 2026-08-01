
def test_transform_agg_by_name(request, reduction_func, frame_or_series):
    func = reduction_func

    obj = DataFrame(
        {"a": [0, 0, 0, 0, 1, 1, 1, 1], "b": range(8)},
        index=["A", "B", "C", "D", "E", "F", "G", "H"],
    )
    if frame_or_series is Series:
        obj = obj["a"]

    g = obj.groupby(np.repeat([0, 1], 4))

    if func == "corrwith" and isinstance(obj, Series):  # GH#32293
        # TODO: implement SeriesGroupBy.corrwith
        assert not hasattr(g, func)
        return

    args = get_groupby_method_args(reduction_func, obj)
    if func == "corrwith":
        warn = Pandas4Warning
        msg = "DataFrameGroupBy.corrwith is deprecated"
    else:
        warn = None
        msg = ""
    with tm.assert_produces_warning(warn, match=msg):
        result = g.transform(func, *args)

    # this is the *definition* of a transformation
    tm.assert_index_equal(result.index, obj.index)

    if func not in ("ngroup", "size") and obj.ndim == 2:
        # size/ngroup return a Series, unlike other transforms
        tm.assert_index_equal(result.columns, obj.columns)

    # verify that values were broadcasted across each group
    assert len(set(DataFrame(result).iloc[-4:, -1])) == 1

