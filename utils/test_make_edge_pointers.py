
def test_make_edge_pointers(a, expected):
    a = csr_array(a, dtype=np.int32)
    rev_edge_ptr = _make_edge_pointers(a)
    assert_array_equal(rev_edge_ptr, expected)

