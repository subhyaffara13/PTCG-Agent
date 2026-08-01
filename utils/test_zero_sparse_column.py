
def test_zero_sparse_column():
    # GH 27781
    df1 = pd.DataFrame({"A": SparseArray([0, 0, 0]), "B": [1, 2, 3]})
    df2 = pd.DataFrame({"A": SparseArray([0, 1, 0]), "B": [1, 2, 3]})
    result = df1.loc[df1["B"] != 2]
    expected = df2.loc[df2["B"] != 2]
    tm.assert_frame_equal(result, expected)

    expected = pd.DataFrame({"A": SparseArray([0, 0]), "B": [1, 3]}, index=[0, 2])
    tm.assert_frame_equal(result, expected)

