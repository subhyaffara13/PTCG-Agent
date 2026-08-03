import re

def test_append_with_different_block_ordering(temp_hdfstore):
    # GH 4096; using same frames, but different block orderings
    for i in range(10):
        df = DataFrame(
            np.random.default_rng(2).standard_normal((10, 2)), columns=list("AB")
        )
        df["index"] = range(10)
        df["index"] += i * 10
        df["int64"] = Series([1] * len(df), dtype="int64")
        df["int16"] = Series([1] * len(df), dtype="int16")

        if i % 2 == 0:
            del df["int64"]
            df["int64"] = Series([1] * len(df), dtype="int64")
        if i % 3 == 0:
            a = df.pop("A")
            df["A"] = a

        df.set_index("index", inplace=True)

        temp_hdfstore.append("df", df)

    # test a different ordering but with more fields (like invalid
    # combinations)
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 2)),
        columns=list("AB"),
        dtype="float64",
    )
    df["int64"] = Series([1] * len(df), dtype="int64")
    df["int16"] = Series([1] * len(df), dtype="int16")
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df)

    # store additional fields in different blocks
    df["int16_2"] = Series([1] * len(df), dtype="int16")
    msg = re.escape(
        "cannot match existing table structure for [int16] on appending data"
    )
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append("df", df)

    # store multiple additional fields in different blocks
    df["float_3"] = Series([1.0] * len(df), dtype="float64")
    msg = re.escape("cannot match existing table structure for [A,B] on appending data")
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append("df", df)

