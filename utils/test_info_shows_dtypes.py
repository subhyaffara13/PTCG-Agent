
def test_info_shows_dtypes():
    dtypes = [
        "int64",
        "float64",
        "datetime64[ns]",
        "timedelta64[ns]",
        "complex128",
        "object",
        "bool",
    ]
    n = 10
    for dtype in dtypes:
        s = Series(np.random.default_rng(2).integers(2, size=n).astype(dtype))
        buf = StringIO()
        s.info(buf=buf)
        res = buf.getvalue()
        name = f"{n:d} non-null     {dtype}"
        assert name in res

