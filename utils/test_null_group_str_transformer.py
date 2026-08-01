
def test_null_group_str_transformer(dropna, transformation_func):
    # GH 17093
    df = DataFrame({"A": [1, 1, np.nan], "B": [1, 2, 2]}, index=[1, 2, 3])
    args = get_groupby_method_args(transformation_func, df)
    gb = df.groupby("A", dropna=dropna)

    buffer = []
    for k, (idx, group) in enumerate(gb):
        if transformation_func == "cumcount":
            # DataFrame has no cumcount method
            res = DataFrame({"B": range(len(group))}, index=group.index)
        elif transformation_func == "ngroup":
            res = DataFrame(len(group) * [k], index=group.index, columns=["B"])
        else:
            res = getattr(group[["B"]], transformation_func)(*args)
        buffer.append(res)
    if dropna:
        dtype = object if transformation_func in ("any", "all") else None
        buffer.append(DataFrame([[np.nan]], index=[3], dtype=dtype, columns=["B"]))
    expected = concat(buffer)

    if transformation_func in ("cumcount", "ngroup"):
        # ngroup/cumcount always returns a Series as it counts the groups, not values
        expected = expected["B"].rename(None)

    result = gb.transform(transformation_func, *args)
    tm.assert_equal(result, expected)

