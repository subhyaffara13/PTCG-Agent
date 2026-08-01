
def test_resample_nunique(unit):
    # GH 12352
    df = DataFrame(
        {
            "ID": {
                Timestamp("2015-06-05 00:00:00"): "0010100903",
                Timestamp("2015-06-08 00:00:00"): "0010150847",
            },
            "DATE": {
                Timestamp("2015-06-05 00:00:00"): "2015-06-05",
                Timestamp("2015-06-08 00:00:00"): "2015-06-08",
            },
        }
    )
    df.index = df.index.as_unit(unit)
    r = df.resample("D")
    g = df.groupby(Grouper(freq="D"))
    expected = df.groupby(Grouper(freq="D")).ID.apply(lambda x: x.nunique())
    assert expected.name == "ID"

    for t in [r, g]:
        result = t.ID.nunique()
        tm.assert_series_equal(result, expected)

    result = df.ID.resample("D").nunique()
    tm.assert_series_equal(result, expected)

    result = df.ID.groupby(Grouper(freq="D")).nunique()
    tm.assert_series_equal(result, expected)

