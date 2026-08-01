
def test_resample_frame_basic_cy_funcs(f, unit):
    df = DataFrame(
        np.random.default_rng(2).standard_normal((50, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=date_range("2000-01-01", periods=50, freq="B"),
    )
    df.index = df.index.as_unit(unit)

    b = Grouper(freq="ME")
    g = df.groupby(b)

    # check all cython functions work
    g._cython_agg_general(f, alt=None, numeric_only=True)

