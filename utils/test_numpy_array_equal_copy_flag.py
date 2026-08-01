
def test_numpy_array_equal_copy_flag(other_type, check_same):
    a = np.array([1, 2, 3])
    msg = None

    if other_type == "same":
        other = a.view()
    else:
        other = a.copy()

    if check_same != other_type:
        msg = (
            r"array\(\[1, 2, 3\]\) is not array\(\[1, 2, 3\]\)"
            if check_same == "same"
            else r"array\(\[1, 2, 3\]\) is array\(\[1, 2, 3\]\)"
        )

    if msg is not None:
        with pytest.raises(AssertionError, match=msg):
            tm.assert_numpy_array_equal(a, other, check_same=check_same)
    else:
        tm.assert_numpy_array_equal(a, other, check_same=check_same)

