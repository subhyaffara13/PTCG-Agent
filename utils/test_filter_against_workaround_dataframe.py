
def test_filter_against_workaround_dataframe():
    # Set up DataFrame of ints, floats, strings.
    letters = np.array(list(ascii_lowercase))
    N = 10
    random_letters = letters.take(
        np.random.default_rng(2).integers(0, 26, N, dtype=int)
    )
    df = DataFrame(
        {
            "ints": Series(np.random.default_rng(2).integers(0, 10, N)),
            "floats": N / 10 * Series(np.random.default_rng(2).random(N)),
            "letters": Series(random_letters),
        }
    )

    # Group by ints; filter on floats.
    grouped = df.groupby("ints")
    old_way = df[grouped.floats.transform(lambda x: x.mean() > N / 2).astype("bool")]
    new_way = grouped.filter(lambda x: x["floats"].mean() > N / 2)
    tm.assert_frame_equal(new_way, old_way)

    # Group by floats (rounded); filter on strings.
    grouper = df.floats.apply(lambda x: np.round(x, -1))
    grouped = df.groupby(grouper)
    old_way = df[grouped.letters.transform(lambda x: len(x) < N / 2).astype("bool")]
    new_way = grouped.filter(lambda x: len(x.letters) < N / 2)
    tm.assert_frame_equal(new_way, old_way)

    # Group by strings; filter on ints.
    grouped = df.groupby("letters")
    old_way = df[grouped.ints.transform(lambda x: x.mean() > N / 2).astype("bool")]
    new_way = grouped.filter(lambda x: x["ints"].mean() > N / 2)
    tm.assert_frame_equal(new_way, old_way)

