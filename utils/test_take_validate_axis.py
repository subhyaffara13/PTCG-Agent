
def test_take_validate_axis():
    # GH#51022
    ser = Series([-1, 5, 6, 2, 4])

    msg = "No axis named foo for object type Series"
    with pytest.raises(ValueError, match=msg):
        ser.take([1, 2], axis="foo")

