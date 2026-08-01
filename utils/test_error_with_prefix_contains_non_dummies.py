
def test_error_with_prefix_contains_non_dummies(dummies_basic):
    # Set object dtype to avoid upcast when setting "str"
    dummies_basic["col2_c"] = dummies_basic["col2_c"].astype(object)
    dummies_basic.loc[2, "col2_c"] = "str"
    with pytest.raises(TypeError, match=r"Passed DataFrame contains non-dummy data"):
        from_dummies(dummies_basic, sep="_")

