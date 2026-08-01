
def test_make_tails(a, expected):
    a = csr_array(a, dtype=np.int32)
    tails = _make_tails(a)
    assert_array_equal(tails, expected)

