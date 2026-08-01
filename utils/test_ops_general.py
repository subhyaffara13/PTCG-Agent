
def test_ops_general(op, targop):
    df = DataFrame(np.random.default_rng(2).standard_normal(1000))
    labels = np.random.default_rng(2).integers(0, 50, size=1000).astype(float)

    result = getattr(df.groupby(labels), op)()
    kwargs = {"ddof": 1, "axis": 0} if op in ["std", "var"] else {}
    expected = df.groupby(labels).agg(targop, **kwargs)
    tm.assert_frame_equal(result, expected)

