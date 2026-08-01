
def test_agg_with_missing_values():
    # GH#58810
    missing_df = DataFrame(
        {
            "nan": [np.nan, np.nan, np.nan, np.nan],
            "na": [pd.NA, pd.NA, pd.NA, pd.NA],
            "nat": [pd.NaT, pd.NaT, pd.NaT, pd.NaT],
            "none": [None, None, None, None],
            "values": [1, 2, 3, 4],
        }
    )

    result = missing_df.agg(x=("nan", "min"), y=("na", "min"), z=("values", "sum"))

    expected = DataFrame(
        {
            "nan": [np.nan, np.nan, np.nan],
            "na": [np.nan, np.nan, np.nan],
            "values": [np.nan, np.nan, 10.0],
        },
        index=["x", "y", "z"],
    )

    tm.assert_frame_equal(result, expected)

