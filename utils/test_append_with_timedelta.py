
def test_append_with_timedelta(temp_hdfstore, unit):
    # GH 3577
    # append timedelta

    ts = Timestamp("20130101").as_unit("ns")
    df = DataFrame(
        {
            "A": ts,
            "B": [ts + timedelta(days=i, seconds=10) for i in range(10)],
        }
    )
    df["C"] = df["A"] - df["B"]
    df["C"] = df["C"].astype(f"m8[{unit}]")
    df.loc[3:5, "C"] = np.nan

    # table
    temp_hdfstore.append("df", df, data_columns=True)
    result = temp_hdfstore.select("df")
    tm.assert_frame_equal(result, df)

    result = temp_hdfstore.select("df", where="C<100000")
    tm.assert_frame_equal(result, df)

    result = temp_hdfstore.select("df", where="C<pd.Timedelta('-3D')")
    tm.assert_frame_equal(result, df.iloc[3:])

    result = temp_hdfstore.select("df", "C<'-3D'")
    tm.assert_frame_equal(result, df.iloc[3:])

    # a bit hacky here as we don't really deal with the NaT properly

    result = temp_hdfstore.select("df", "C<'-500000s'")
    result = result.dropna(subset=["C"])
    tm.assert_frame_equal(result, df.iloc[6:])

    result = temp_hdfstore.select("df", "C<'-3.5D'")
    result = result.iloc[1:]
    tm.assert_frame_equal(result, df.iloc[4:])

    # fixed
    temp_hdfstore.put("df2", df)
    result = temp_hdfstore.select("df2")
    tm.assert_frame_equal(result, df)

