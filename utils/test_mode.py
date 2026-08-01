
def test_mode():
    expr = x + y
    assert latex(expr) == r'x + y'
    assert latex(expr, mode='plain') == r'x + y'
    assert latex(expr, mode='inline') == r'$x + y$'
    assert latex(
        expr, mode='equation*') == r'\begin{equation*}x + y\end{equation*}'
    assert latex(
        expr, mode='equation') == r'\begin{equation}x + y\end{equation}'
    raises(ValueError, lambda: latex(expr, mode='foo'))


def test_mode(dtype, shape, axis, xp):
    mxp, marrays, narrays = get_arrays(1, shape=shape, all_unique=False, xp=xp)
    res = stats.mode(mxp.astype(marrays[0], getattr(mxp, dtype)))
    ref = stats.mode(*narrays, nan_policy='omit')
    xp_assert_close(res.mode.data, xp.asarray(ref.mode.astype(dtype)))
    xp_assert_close(res.count.data, xp.asarray(ref.count))


def test_mode(temp_h5_path, mode, using_infer_string):
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    msg = r"[\S]* does not exist"
    doesnt_exist = f"{uuid.uuid4()}.h5"

    # constructor
    if mode in ["r", "r+"]:
        with pytest.raises(OSError, match=msg):
            HDFStore(doesnt_exist, mode=mode)

    else:
        with HDFStore(temp_h5_path, mode=mode) as store:
            assert store._handle.mode == mode

    # context
    if mode in ["r", "r+"]:
        with pytest.raises(OSError, match=msg):
            with HDFStore(doesnt_exist, mode=mode) as store:
                pass
    else:
        with HDFStore(temp_h5_path, mode=mode) as store:
            assert store._handle.mode == mode

    # conv write
    if mode in ["r", "r+"]:
        with pytest.raises(OSError, match=msg):
            df.to_hdf(doesnt_exist, key="df", mode=mode)
        df.to_hdf(temp_h5_path, key="df", mode="w")
    else:
        df.to_hdf(temp_h5_path, key="df", mode=mode)

    # conv read
    if mode in ["w"]:
        msg = (
            "mode w is not allowed while performing a read. "
            r"Allowed modes are r, r\+ and a."
        )
        with pytest.raises(ValueError, match=msg):
            read_hdf(temp_h5_path, "df", mode=mode)
    else:
        result = read_hdf(temp_h5_path, "df", mode=mode)
        if using_infer_string:
            df.columns = df.columns.astype("str")
        tm.assert_frame_equal(result, df)

