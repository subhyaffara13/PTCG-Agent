
def test_merge_for_suffix_collisions(suffixes):
    # GH#61402
    df1 = DataFrame({"col1": [1], "col2": [2]})
    df2 = DataFrame({"col1": [1], "col2": [2], "col2_dup": [3]})
    with pytest.raises(MergeError, match="duplicate columns"):
        merge(df1, df2, on="col1", suffixes=suffixes)

