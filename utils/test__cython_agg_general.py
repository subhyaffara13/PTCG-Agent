
def test__cython_agg_general(op, targop):
    df = DataFrame(np.random.default_rng(2).standard_normal(1000))
    labels = np.random.default_rng(2).integers(0, 50, size=1000).astype(float)
    kwargs = {"ddof": 1} if op == "var" else {}
    if op not in ["first", "last"]:
        kwargs["axis"] = 0

    result = df.groupby(labels)._cython_agg_general(op, alt=None, numeric_only=True)
    expected = df.groupby(labels).agg(targop, **kwargs)
    tm.assert_frame_equal(result, expected)

