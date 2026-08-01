
def test_downcast_empty(dc1, dc2):
    # GH32493

    tm.assert_numpy_array_equal(
        to_numeric([], downcast=dc1),
        to_numeric([], downcast=dc2),
        check_dtype=False,
    )

