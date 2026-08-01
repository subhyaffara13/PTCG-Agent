
def test_error_with_prefix_contains_nan(dummies_basic):
    # Set float64 dtype to avoid upcast when setting np.nan
    dummies_basic["col2_c"] = dummies_basic["col2_c"].astype("float64")
    dummies_basic.loc[2, "col2_c"] = np.nan
    with pytest.raises(
        ValueError, match=r"Dummy DataFrame contains NA value in column: 'col2_c'"
    ):
        from_dummies(dummies_basic, sep="_")

