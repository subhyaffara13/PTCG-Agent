
def test_append(temp_hdfstore):
    # this is allowed by almost always don't want to do it
    # tables.NaturalNameWarning):
    df = DataFrame(
        np.random.default_rng(2).standard_normal((20, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=20, freq="B"),
    )
    temp_hdfstore.append("df1", df[:10])
    temp_hdfstore.append("df1", df[10:])
    tm.assert_frame_equal(temp_hdfstore["df1"], df)

    temp_hdfstore.put("df2", df[:10], format="table")
    temp_hdfstore.append("df2", df[10:])
    tm.assert_frame_equal(temp_hdfstore["df2"], df)

    temp_hdfstore.append("/df3", df[:10])
    temp_hdfstore.append("/df3", df[10:])
    tm.assert_frame_equal(temp_hdfstore["df3"], df)

    # this is allowed by almost always don't want to do it
    # tables.NaturalNameWarning
    temp_hdfstore.append("/df3 foo", df[:10])
    temp_hdfstore.append("/df3 foo", df[10:])
    tm.assert_frame_equal(temp_hdfstore["df3 foo"], df)

    # dtype issues - mizxed type in a single object column
    df = DataFrame(data=[[1, 2], [0, 1], [1, 2], [0, 0]])
    df["mixed_column"] = "testing"
    df.loc[2, "mixed_column"] = np.nan
    temp_hdfstore.append("df", df)
    tm.assert_frame_equal(temp_hdfstore["df"], df)

    # uints - test storage of uints
    uint_data = DataFrame(
        {
            "u08": Series(
                np.random.default_rng(2).integers(0, high=255, size=5),
                dtype=np.uint8,
            ),
            "u16": Series(
                np.random.default_rng(2).integers(0, high=65535, size=5),
                dtype=np.uint16,
            ),
            "u32": Series(
                np.random.default_rng(2).integers(0, high=2**30, size=5),
                dtype=np.uint32,
            ),
            "u64": Series(
                [2**58, 2**59, 2**60, 2**61, 2**62],
                dtype=np.uint64,
            ),
        },
        index=np.arange(5),
    )
    temp_hdfstore.append("uints", uint_data)
    tm.assert_frame_equal(temp_hdfstore["uints"], uint_data, check_index_type=True)

    # uints - test storage of uints in indexable columns
    temp_hdfstore.remove("uints")
    # 64-bit indices not yet supported
    temp_hdfstore.append("uints", uint_data, data_columns=["u08", "u16", "u32"])
    tm.assert_frame_equal(temp_hdfstore["uints"], uint_data, check_index_type=True)


def test_append(idx):
    result = idx[:3].append(idx[3:])
    assert result.equals(idx)

    foos = [idx[:1], idx[1:3], idx[3:]]
    result = foos[0].append(foos[1:])
    assert result.equals(idx)

    # empty
    result = idx.append([])
    assert result.equals(idx)

