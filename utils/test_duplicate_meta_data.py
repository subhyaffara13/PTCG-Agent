
def test_duplicate_meta_data():
    # GH 10115
    mi = MultiIndex(
        levels=[[0, 1], [0, 1, 2]], codes=[[0, 0, 0, 0, 1, 1, 1], [0, 1, 2, 0, 0, 1, 2]]
    )

    for idx in [
        mi,
        mi.set_names([None, None]),
        mi.set_names([None, "Num"]),
        mi.set_names(["Upper", "Num"]),
    ]:
        assert idx.has_duplicates
        assert idx.drop_duplicates().names == idx.names

