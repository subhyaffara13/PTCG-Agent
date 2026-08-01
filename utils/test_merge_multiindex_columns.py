
def test_merge_multiindex_columns():
    # Issue #28518
    # Verify that merging two dataframes give the expected labels
    # The original cause of this issue come from a bug lexsort_depth and is tested in
    # test_lexsort_depth

    letters = ["a", "b", "c", "d"]
    numbers = ["1", "2", "3"]
    index = MultiIndex.from_product((letters, numbers), names=["outer", "inner"])

    frame_x = DataFrame(columns=index)
    frame_x["id"] = ""
    frame_y = DataFrame(columns=index)
    frame_y["id"] = ""

    l_suf = "_x"
    r_suf = "_y"
    result = frame_x.merge(frame_y, on="id", suffixes=((l_suf, r_suf)))

    # Constructing the expected results
    tuples = [(letter + l_suf, num) for letter in letters for num in numbers]
    tuples += [("id", "")]
    tuples += [(letter + r_suf, num) for letter in letters for num in numbers]

    expected_index = MultiIndex.from_tuples(tuples, names=["outer", "inner"])
    expected = DataFrame(columns=expected_index)

    tm.assert_frame_equal(result, expected, check_dtype=False)

