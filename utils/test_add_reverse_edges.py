
def test_add_reverse_edges(a, b_data_expected):
    """Test that the reversal of the edges of the input graph works
    as expected.
    """
    a = csr_array(a, dtype=np.int32, shape=(len(a), len(a)))
    b = _add_reverse_edges(a)
    assert_array_equal(b.data, b_data_expected)

