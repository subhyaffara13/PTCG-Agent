
def test_loc_getitem_duplicates_multiindex_non_scalar_type_object():
    # regression from < 0.14.0
    # GH 7914
    df = DataFrame(
        [[np.mean, np.median], ["mean", "median"]],
        columns=MultiIndex.from_tuples([("functs", "mean"), ("functs", "median")]),
        index=["function", "name"],
    )
    result = df.loc["function", ("functs", "mean")]
    expected = np.mean
    assert result == expected

