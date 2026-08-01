
def test_transform_axis_1_raises():
    # GH 35964
    msg = "No axis named 1 for object type Series"
    with pytest.raises(ValueError, match=msg):
        Series([1]).transform("sum", axis=1)

