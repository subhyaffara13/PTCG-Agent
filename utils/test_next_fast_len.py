
def test_next_fast_len():
    for n in _5_smooth_numbers:
        assert_equal(next_fast_len(n), n)

