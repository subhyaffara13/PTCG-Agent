
def test_no_sort_keep_na(sequence, dtype, test_series, as_index):
    # GH#46584, GH#48794

    # Unique values to use for grouper, depends on dtype
    if dtype in ("string", "string[pyarrow]"):
        uniques = {"x": "x", "y": "y", "z": pd.NA}
    elif dtype in ("datetime64[ns]", "period[D]"):
        uniques = {"x": "2016-01-01", "y": "2017-01-01", "z": pd.NA}
    elif dtype is not None and dtype.startswith(("I", "U", "F")):
        uniques = {"x": 1, "y": 2, "z": pd.NA}
    else:
        uniques = {"x": 1, "y": 2, "z": np.nan}

    df = pd.DataFrame(
        {
            "key": pd.Series([uniques[label] for label in sequence], dtype=dtype),
            "a": [0, 1, 2, 3],
        }
    )
    gb = df.groupby("key", dropna=False, sort=False, as_index=as_index, observed=False)
    if test_series:
        gb = gb["a"]
    result = gb.sum()

    # Manually compute the groupby sum, use the labels "x", "y", and "z" to avoid
    # issues with hashing np.nan
    summed = {}
    for idx, label in enumerate(sequence):
        summed[label] = summed.get(label, 0) + idx
    if dtype == "category":
        index = pd.CategoricalIndex(
            [uniques[e] for e in summed],
            df["key"].cat.categories,
            name="key",
        )
    elif isinstance(dtype, str) and dtype.startswith("Sparse"):
        index = pd.Index(
            pd.array([uniques[label] for label in summed], dtype=dtype), name="key"
        )
    else:
        index = pd.Index([uniques[label] for label in summed], dtype=dtype, name="key")
    expected = pd.Series(summed.values(), index=index, name="a", dtype=None)
    if not test_series:
        expected = expected.to_frame()
    if not as_index:
        expected = expected.reset_index()
        if dtype is not None and dtype.startswith("Sparse"):
            expected["key"] = expected["key"].astype(dtype)

    tm.assert_equal(result, expected)

