
def test_info_categorical_column_just_works():
    n = 2500
    data = np.array(list("abcdefghij")).take(
        np.random.default_rng(2).integers(0, 10, size=n, dtype=int)
    )
    s = Series(data).astype("category")
    s.isna()
    buf = StringIO()
    s.info(buf=buf)

    s2 = s[s == "d"]
    buf = StringIO()
    s2.info(buf=buf)

