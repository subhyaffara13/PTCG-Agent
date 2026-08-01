
def test_mi_columns_loc_list_label_order():
    # GH 10710
    cols = MultiIndex.from_product([["A", "B", "C"], [1, 2]])
    df = DataFrame(np.zeros((5, 6)), columns=cols)
    result = df.loc[:, ["B", "A"]]
    expected = DataFrame(
        np.zeros((5, 4)),
        columns=MultiIndex.from_tuples([("B", 1), ("B", 2), ("A", 1), ("A", 2)]),
    )
    tm.assert_frame_equal(result, expected)

