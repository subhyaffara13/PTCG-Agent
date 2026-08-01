
def test_value_indices02(xp):
    "Test input checking"
    data = xp.zeros((5, 4), dtype=xp.float32)
    msg = "Parameter 'arr' must be an integer array"
    with assert_raises(ValueError, match=msg):
        ndimage.value_indices(data)

