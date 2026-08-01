
def test_transform_fast():
    df = DataFrame(
        {
            "id": np.arange(10) / 3,
            "val": np.random.default_rng(2).standard_normal(10),
        }
    )

    grp = df.groupby("id")["val"]

    values = np.repeat(grp.mean().values, ensure_platform_int(grp.count().values))
    expected = Series(values, index=df.index, name="val")

    result = grp.transform(np.mean)
    tm.assert_series_equal(result, expected)

    result = grp.transform("mean")
    tm.assert_series_equal(result, expected)

