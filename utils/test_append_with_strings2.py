
def test_append_with_strings2(temp_hdfstore):
    def check_col(key, name, size):
        assert (
            getattr(temp_hdfstore.get_storer(key).table.description, name).itemsize
            == size
        )

    df = DataFrame({"A": "foo", "B": "bar"}, index=range(10))

    # a min_itemsize that creates a data_column
    temp_hdfstore.append("df", df, min_itemsize={"A": 200})
    check_col("df", "A", 200)
    assert temp_hdfstore.get_storer("df").data_columns == ["A"]

    # a min_itemsize that creates a data_column2
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df, data_columns=["B"], min_itemsize={"A": 200})
    check_col("df", "A", 200)
    assert temp_hdfstore.get_storer("df").data_columns == ["B", "A"]

    # a min_itemsize that creates a data_column2
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df, data_columns=["B"], min_itemsize={"values": 200})
    check_col("df", "B", 200)
    check_col("df", "values_block_0", 200)
    assert temp_hdfstore.get_storer("df").data_columns == ["B"]

    # infer the .typ on subsequent appends
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df[:5], min_itemsize=200)
    temp_hdfstore.append("df", df[5:], min_itemsize=200)
    tm.assert_frame_equal(temp_hdfstore["df"], df)

    # invalid min_itemsize keys
    df = DataFrame(["foo", "foo", "foo", "barh", "barh", "barh"], columns=["A"])
    temp_hdfstore.remove("df")
    msg = re.escape(
        "min_itemsize has the key [foo] which is not an axis or data_column"
    )
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append("df", df, min_itemsize={"foo": 20, "foobar": 20})

