
def test_merge_cross_error_reporting(kwargs):
    # GH#5401
    left = DataFrame({"a": [1, 3]})
    right = DataFrame({"b": [3, 4]})
    msg = (
        "Can not pass on, right_on, left_on or set right_index=True or left_index=True"
    )
    with pytest.raises(MergeError, match=msg):
        merge(left, right, how="cross", **kwargs)

