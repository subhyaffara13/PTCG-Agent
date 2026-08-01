
def test_groupby_agg_extension_timedelta_cumsum_with_named_aggregation():
    # GH#41720
    expected = DataFrame(
        {
            "td": {
                0: pd.Timedelta("0 days 01:00:00"),
                1: pd.Timedelta("0 days 01:15:00"),
                2: pd.Timedelta("0 days 01:15:00"),
            }
        }
    )
    df = DataFrame(
        {
            "td": Series(
                ["0 days 01:00:00", "0 days 00:15:00", "0 days 01:15:00"],
                dtype="timedelta64[us]",
            ),
            "grps": ["a", "a", "b"],
        }
    )
    gb = df.groupby("grps")
    result = gb.agg(td=("td", "cumsum"))
    tm.assert_frame_equal(result, expected)

