
def test_groupby_resample_size_all_index_same():
    # GH 46826
    df = DataFrame(
        {"A": [1] * 3 + [2] * 3 + [1] * 3 + [2] * 3, "B": np.arange(12)},
        index=date_range("31/12/2000 18:00", freq="h", periods=12, unit="ns"),
    )
    result = df.groupby("A").resample("D").size()

    mi_exp = pd.MultiIndex.from_arrays(
        [
            [1, 1, 2, 2],
            pd.DatetimeIndex(["2000-12-31", "2001-01-01"] * 2, dtype="M8[ns]"),
        ],
        names=["A", None],
    )
    expected = Series(
        3,
        index=mi_exp,
    )
    tm.assert_series_equal(result, expected)

