
def test_remove_unused_levels_large(first_type, second_type):
    # GH16556

    # because tests should be deterministic (and this test in particular
    # checks that levels are removed, which is not the case for every
    # random input):
    rng = np.random.default_rng(10)  # seed is arbitrary value that works

    size = 1 << 16
    df = DataFrame(
        {
            "first": rng.integers(0, 1 << 13, size).astype(first_type),
            "second": rng.integers(0, 1 << 10, size).astype(second_type),
            "third": rng.random(size),
        }
    )
    df = df.groupby(["first", "second"]).sum()
    df = df[df.third < 0.1]

    result = df.index.remove_unused_levels()
    assert len(result.levels[0]) < len(df.index.levels[0])
    assert len(result.levels[1]) < len(df.index.levels[1])
    assert result.equals(df.index)

    expected = df.reset_index().set_index(["first", "second"]).index
    tm.assert_index_equal(result, expected)

