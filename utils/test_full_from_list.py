
def test_full_from_list(shape, fill_value, expected_output):
    output = np.full(shape, fill_value)
    assert_equal(output, expected_output)

