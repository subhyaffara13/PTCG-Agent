
def test_groupby_dropna_datetime_like_data(
    dropna, values, datetime1, datetime2, unique_nulls_fixture, unique_nulls_fixture2
):
    # 3729
    df = pd.DataFrame(
        {
            "values": [1, 2, 3, 4, 5, 6],
            "dt": [
                datetime1,
                unique_nulls_fixture,
                datetime2,
                unique_nulls_fixture2,
                datetime1,
                datetime1,
            ],
        }
    )

    if dropna:
        indexes = [datetime1, datetime2]
    else:
        indexes = [datetime1, datetime2, np.nan]

    grouped = df.groupby("dt", dropna=dropna).agg({"values": "sum"})
    expected = pd.DataFrame({"values": values}, index=pd.Index(indexes, name="dt"))

    tm.assert_frame_equal(grouped, expected)

