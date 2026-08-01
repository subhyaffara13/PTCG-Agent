
def test_object_input(mode):
    # Regression test for issue gh-11395.
    a = np.full((4, 3), fill_value=None)
    pad_amt = ((2, 3), (3, 2))
    b = np.full((9, 8), fill_value=None)
    assert_array_equal(np.pad(a, pad_amt, mode=mode), b)

