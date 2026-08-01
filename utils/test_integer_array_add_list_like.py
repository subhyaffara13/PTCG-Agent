
def test_integer_array_add_list_like(
    box_pandas_1d_array, box_1d_array, data, expected_data
):
    # GH22606 Verify operators with IntegerArray and list-likes
    arr = array(data, dtype="Int64")
    container = box_pandas_1d_array(arr)
    left = container + box_1d_array(data)
    right = box_1d_array(data) + container

    if Series in [box_1d_array, box_pandas_1d_array]:
        cls = Series
    elif Index in [box_1d_array, box_pandas_1d_array]:
        cls = Index
    else:
        cls = array

    expected = cls(expected_data, dtype="Int64")

    tm.assert_equal(left, expected)
    tm.assert_equal(right, expected)

