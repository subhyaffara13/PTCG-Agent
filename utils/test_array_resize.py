
def test_array_resize():
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype="float64")
    m.array_reshape2(a)
    assert a.size == 9
    assert np.all(a == [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    # total size change should succced with refcheck off
    m.array_resize3(a, 4, False)
    assert a.size == 64
    # ... and fail with refcheck on
    try:
        m.array_resize3(a, 3, True)
    except ValueError as e:
        assert str(e).startswith("cannot resize an array")  # noqa: PT017
    # transposed array doesn't own data
    b = a.transpose()
    try:
        m.array_resize3(b, 3, False)
    except ValueError as e:
        assert str(e).startswith(  # noqa: PT017
            "cannot resize this array: it does not own its data"
        )
    # ... but reshape should be fine
    m.array_reshape2(b)
    assert b.shape == (8, 8)

