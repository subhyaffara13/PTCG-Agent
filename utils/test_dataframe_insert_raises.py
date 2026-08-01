
def test_dataframe_insert_raises():
    df = pd.DataFrame({"A": [1, 2]}).set_flags(allows_duplicate_labels=False)
    msg = "Cannot specify"
    with pytest.raises(ValueError, match=msg):
        df.insert(0, "A", [3, 4], allow_duplicates=True)

