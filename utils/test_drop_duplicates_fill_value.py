
def test_drop_duplicates_fill_value():
    # GH 11726
    df = pd.DataFrame(np.zeros((5, 5))).apply(lambda x: SparseArray(x, fill_value=0))
    result = df.drop_duplicates()
    expected = pd.DataFrame({i: SparseArray([0.0], fill_value=0) for i in range(5)})
    tm.assert_frame_equal(result, expected)

