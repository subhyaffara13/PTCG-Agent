
def test_max_sas_date_iterator(datapath):
    # GH 20927
    # when called as an iterator, only those chunks with a date > pd.Timestamp.max
    # are returned as datetime.datetime, if this happens that whole chunk is returned
    # as datetime.datetime
    col_order = ["text", "dt_as_float", "dt_as_dt", "date_as_float", "date_as_date"]
    fname = datapath("io", "sas", "data", "max_sas_date.sas7bdat")
    results = []
    for df in pd.read_sas(fname, encoding="iso-8859-1", chunksize=1):
        # GH 19732: Timestamps imported from sas will incur floating point errors
        df.reset_index(inplace=True, drop=True)
        results.append(df)
    expected = [
        pd.DataFrame(
            {
                "text": ["max"],
                "dt_as_float": [253717747199.999],
                "dt_as_dt": np.array(
                    [datetime(9999, 12, 29, 23, 59, 59, 999000)], dtype="M8[ms]"
                ),
                "date_as_float": [2936547.0],
                "date_as_date": np.array([datetime(9999, 12, 29)], dtype="M8[s]"),
            },
            columns=col_order,
        ),
        pd.DataFrame(
            {
                "text": ["normal"],
                "dt_as_float": [1880323199.999],
                "dt_as_dt": np.array(["2019-08-01 23:59:59.999"], dtype="M8[ms]"),
                "date_as_float": [21762.0],
                "date_as_date": np.array(["2019-08-01"], dtype="M8[s]"),
            },
            columns=col_order,
        ),
    ]
    if not IS64:
        # No good reason for this, just what we get on the CI
        expected[0].loc[0, "dt_as_dt"] -= np.timedelta64(1, "ms")
        expected[1].loc[0, "dt_as_dt"] -= np.timedelta64(1, "ms")

    tm.assert_frame_equal(results[0], expected[0])
    tm.assert_frame_equal(results[1], expected[1])

