
def test_suffix_on_list_join():
    first = DataFrame({"key": [1, 2, 3, 4, 5]})
    second = DataFrame({"key": [1, 8, 3, 2, 5], "v1": [1, 2, 3, 4, 5]})
    third = DataFrame({"keys": [5, 2, 3, 4, 1], "v2": [1, 2, 3, 4, 5]})

    # check proper errors are raised
    msg = "Suffixes not supported when joining multiple DataFrames"
    with pytest.raises(ValueError, match=msg):
        first.join([second], lsuffix="y")
    with pytest.raises(ValueError, match=msg):
        first.join([second, third], rsuffix="x")
    with pytest.raises(ValueError, match=msg):
        first.join([second, third], lsuffix="y", rsuffix="x")
    with pytest.raises(ValueError, match="Indexes have overlapping values"):
        first.join([second, third])

    # no errors should be raised
    arr_joined = first.join([third])
    norm_joined = first.join(third)
    tm.assert_frame_equal(arr_joined, norm_joined)

