
def test_equals_mismatched_nas(nulls_fixture, nulls_fixture2):
    # GH#39650
    left = nulls_fixture
    right = nulls_fixture2
    if hasattr(right, "copy"):
        right = right.copy()
    else:
        right = copy.copy(right)

    ser = Series([left], dtype=object)
    ser2 = Series([right], dtype=object)

    if is_matching_na(left, right):
        assert ser.equals(ser2)
    elif (left is None and is_float(right)) or (right is None and is_float(left)):
        assert ser.equals(ser2)
    else:
        assert not ser.equals(ser2)

