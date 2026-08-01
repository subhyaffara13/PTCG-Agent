
def test_null_date(datapath):
    fname = datapath("io", "sas", "data", "dates_null.sas7bdat")
    df = pd.read_sas(fname, encoding="utf-8")

    expected = pd.DataFrame(
        {
            "datecol": np.array(
                [
                    datetime(9999, 12, 29),
                    np.datetime64("NaT", "ns"),
                ],
                dtype="M8[s]",
            ),
            "datetimecol": np.array(
                [
                    datetime(9999, 12, 29, 23, 59, 59, 999000),
                    np.datetime64("NaT", "ns"),
                ],
                dtype="M8[ms]",
            ),
        },
    )
    if not IS64:
        # No good reason for this, just what we get on the CI
        expected.loc[0, "datetimecol"] -= np.timedelta64(1, "ms")
    tm.assert_frame_equal(df, expected)

