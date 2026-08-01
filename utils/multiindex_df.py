
def multiindex_df():
    levels = [["A", ""], ["B", "b"]]
    return DataFrame([[0, 2], [1, 3]], columns=MultiIndex.from_tuples(levels))

