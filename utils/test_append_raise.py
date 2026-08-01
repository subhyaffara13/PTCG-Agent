
def test_append_raise(temp_hdfstore, using_infer_string):
    # test append with invalid input to get good error messages

    # list in column
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )
    df["invalid"] = [["a"]] * len(df)
    assert df.dtypes["invalid"] == np.object_
    msg = re.escape(
        """Cannot serialize the column [invalid]
because its data contents are not [string] but [mixed] object dtype"""
    )
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.append("df", df)

    # multiple invalid columns
    df["invalid2"] = [["a"]] * len(df)
    df["invalid3"] = [["a"]] * len(df)
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.append("df", df)

    # datetime with embedded nans as object
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )
    s = Series(datetime.datetime(2001, 1, 2), index=df.index)
    s = s.astype(object)
    s[0:5] = np.nan
    df["invalid"] = s
    assert df.dtypes["invalid"] == np.object_
    msg = "too many timezones in this block, create separate data columns"
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.append("df", df)

    # directly ndarray
    msg = "value must be None, Series, or DataFrame"
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.append("df", np.arange(10))

    # series directly
    msg = re.escape(
        "cannot properly create the storer for: "
        "[group->df,value-><class 'pandas.Series'>]"
    )
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.append("df", Series(np.arange(10)))

    # appending an incompatible table
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )
    temp_hdfstore.append("df", df)

    df["foo"] = "foo"
    msg = re.escape(
        "invalid combination of [non_index_axes] on appending data "
        "[(1, ['A', 'B', 'C', 'D', 'foo'])] vs current table "
        "[(1, ['A', 'B', 'C', 'D'])]"
    )
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append("df", df)

    # incompatible type (GH 41897)
    df["foo"] = Timestamp("20130101")
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df)
    df["foo"] = "bar"
    msg = re.escape(
        "Cannot serialize the column [foo] "
        "because its data contents are not [string] "
        "but [datetime64[us]] object dtype"
    )
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append("df", df)

