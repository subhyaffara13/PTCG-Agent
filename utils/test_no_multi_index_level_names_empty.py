
def test_no_multi_index_level_names_empty(temp_file, all_parsers):
    # GH 10984
    parser = all_parsers
    midx = MultiIndex.from_tuples([("A", 1, 2), ("A", 1, 2), ("B", 1, 2)])
    expected = DataFrame(
        np.random.default_rng(2).standard_normal((3, 3)),
        index=midx,
        columns=["x", "y", "z"],
    )
    expected.to_csv(temp_file)
    result = parser.read_csv(temp_file, index_col=[0, 1, 2])
    tm.assert_frame_equal(result, expected)

