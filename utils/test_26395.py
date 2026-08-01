
def test_26395(indexer_al):
    # .at case fixed by GH#45121 (best guess)
    df = DataFrame(index=["A", "B", "C"])
    df["D"] = 0

    indexer_al(df)["C", "D"] = 2
    expected = DataFrame({"D": [0, 0, 2]}, index=["A", "B", "C"], dtype=np.int64)
    tm.assert_frame_equal(df, expected)

    with pytest.raises(TypeError, match="Invalid value"):
        indexer_al(df)["C", "D"] = 44.5

    with pytest.raises(TypeError, match="Invalid value"):
        indexer_al(df)["C", "D"] = "hello"

