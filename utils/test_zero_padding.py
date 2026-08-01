
def test_zero_padding():
    """ Ensure that the implicit zero-padding does not cause problems.
    """
    # Ensure that large integers are inserted in little-endian fashion to avoid
    # trailing 0s.
    ss0 = SeedSequence(42)
    ss1 = SeedSequence(42 << 32)
    assert_array_compare(
        np.not_equal,
        ss0.generate_state(4),
        ss1.generate_state(4))

    # Ensure backwards compatibility with the original 0.17 release for small
    # integers and no spawn key.
    expected42 = np.array([3444837047, 2669555309, 2046530742, 3581440988],
                          dtype=np.uint32)
    assert_array_equal(SeedSequence(42).generate_state(4), expected42)

    # Regression test for gh-16539 to ensure that the implicit 0s don't
    # conflict with spawn keys.
    assert_array_compare(
        np.not_equal,
        SeedSequence(42, spawn_key=(0,)).generate_state(4),
        expected42)

