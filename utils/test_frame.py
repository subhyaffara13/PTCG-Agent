
def test_frame():
    return DataFrame(
        {"A": [1] * 20 + [2] * 12 + [3] * 8, "B": np.arange(40)},
        index=date_range("1/1/2000", freq="s", periods=40, unit="ns"),
    )


def test_frame(dti, _test_series):
    return DataFrame({"A": _test_series, "B": _test_series, "C": np.arange(len(dti))})


def test_frame(raw, frame):
    result = frame.rolling(50).apply(f, raw=raw)
    assert isinstance(result, DataFrame)
    tm.assert_series_equal(
        result.iloc[-1, :],
        frame.iloc[-50:, :].apply(np.mean, axis=0, raw=raw),
        check_names=False,
    )


def test_frame(raw, frame, compare_func, roll_func, kwargs, step):
    result = getattr(frame.rolling(50, step=step), roll_func)(**kwargs)
    assert isinstance(result, DataFrame)
    end = range(0, len(frame), step or 1)[-1] + 1
    tm.assert_series_equal(
        result.iloc[-1, :],
        frame.iloc[end - 50 : end, :].apply(compare_func, axis=0, raw=raw),
        check_names=False,
    )


def test_frame(raw, frame, q, step):
    compare_func = partial(scoreatpercentile, per=q)
    result = frame.rolling(50, step=step).quantile(q)
    assert isinstance(result, DataFrame)
    end = range(0, len(frame), step or 1)[-1] + 1
    tm.assert_series_equal(
        result.iloc[-1, :],
        frame.iloc[end - 50 : end, :].apply(compare_func, axis=0, raw=raw),
        check_names=False,
    )


def test_frame(raw, frame, sp_func, roll_func):
    sp_stats = pytest.importorskip("scipy.stats")

    compare_func = partial(getattr(sp_stats, sp_func), bias=False)
    result = getattr(frame.rolling(50), roll_func)()
    assert isinstance(result, DataFrame)
    tm.assert_series_equal(
        result.iloc[-1, :],
        frame.iloc[-50:, :].apply(compare_func, axis=0, raw=raw),
        check_names=False,
    )


def test_frame(compression, temp_h5_path):
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )

    # put in some random NAs
    df.iloc[0, 0] = np.nan
    df.iloc[5, 3] = np.nan

    _check_roundtrip_table(
        df, tm.assert_frame_equal, path=temp_h5_path, compression=compression
    )
    _check_roundtrip(
        df, tm.assert_frame_equal, path=temp_h5_path, compression=compression
    )

    tdf = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    _check_roundtrip(
        tdf, tm.assert_frame_equal, path=temp_h5_path, compression=compression
    )

    with HDFStore(temp_h5_path) as store:
        # not consolidated
        df["foo"] = np.random.default_rng(2).standard_normal(len(df))
        store["df"] = df
        recons = store["df"]
        assert recons._mgr.is_consolidated()

    # empty
    df2 = df[:0]
    # Prevent df2 from having index with inferred_type as string
    df2.index = Index([])
    _check_roundtrip(df2[:0], tm.assert_frame_equal, path=temp_h5_path)


def test_frame(data, all_arithmetic_operators):
    data, scalar = data
    op = tm.get_op_from_name(all_arithmetic_operators)
    check_skip(data, all_arithmetic_operators)

    # DataFrame with scalar
    df = pd.DataFrame({"A": data})

    if is_bool_not_implemented(data, all_arithmetic_operators):
        msg = "operator '.*' not implemented for bool dtypes"
        with pytest.raises(NotImplementedError, match=msg):
            op(df, scalar)
        with pytest.raises(NotImplementedError, match=msg):
            op(data, scalar)
        return

    result = op(df, scalar)
    expected = pd.DataFrame({"A": op(data, scalar)})
    tm.assert_frame_equal(result, expected)

