
def test_apply_empty_infer_type(ax, func, raw, axis, engine, request):
    df = DataFrame(**{ax: ["a", "b", "c"]})

    with np.errstate(all="ignore"):
        test_res = func(np.array([], dtype="f8"))
        is_reduction = not isinstance(test_res, np.ndarray)

        result = df.apply(func, axis=axis, engine=engine, raw=raw)
        if is_reduction:
            agg_axis = df._get_agg_axis(axis)
            assert isinstance(result, Series)
            assert result.index is agg_axis
        else:
            assert isinstance(result, DataFrame)

