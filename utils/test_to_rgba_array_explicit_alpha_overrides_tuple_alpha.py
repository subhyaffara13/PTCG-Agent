
def test_to_rgba_array_explicit_alpha_overrides_tuple_alpha():
    assert_array_equal(
        mcolors.to_rgba_array(('black', 0.9), alpha=0.5),
        [[0, 0, 0, 0.5]])

