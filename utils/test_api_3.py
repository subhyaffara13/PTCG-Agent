
def test_api_3(temp_hdfstore):
    df = DataFrame(range(20))

    temp_hdfstore.append("df", df.iloc[:10], append=True, format="table")
    temp_hdfstore.append("df", df.iloc[10:], append=True, format="table")
    tm.assert_frame_equal(temp_hdfstore.select("df"), df)

    # append to False
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df.iloc[:10], append=False, format="table")
    temp_hdfstore.append("df", df.iloc[10:], append=True, format="table")
    tm.assert_frame_equal(temp_hdfstore.select("df"), df)

    # formats
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df.iloc[:10], append=False, format="table")
    temp_hdfstore.append("df", df.iloc[10:], append=True, format="table")
    tm.assert_frame_equal(temp_hdfstore.select("df"), df)

    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df.iloc[:10], append=False, format="table")
    temp_hdfstore.append("df", df.iloc[10:], append=True, format=None)
    tm.assert_frame_equal(temp_hdfstore.select("df"), df)

