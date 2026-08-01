
def test_in_place_multiply_no_overflow(dt):
    # see gh-30495
    a = np.array("a", dtype=dt)
    a *= 20
    assert_array_equal(a, np.array("a", dtype=dt))

