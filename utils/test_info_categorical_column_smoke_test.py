
def test_info_categorical_column_smoke_test():
    n = 2500
    df = DataFrame({"int64": np.random.default_rng(2).integers(100, size=n, dtype=int)})
    df["category"] = Series(
        np.array(list("abcdefghij")).take(
            np.random.default_rng(2).integers(0, 10, size=n, dtype=int)
        )
    ).astype("category")
    df.isna()
    buf = StringIO()
    df.info(buf=buf)

    df2 = df[df["category"] == "d"]
    buf = StringIO()
    df2.info(buf=buf)

