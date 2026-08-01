
def _assert_match(result_fill_value, expected_fill_value):
    # GH#23982/25425 require the same type in addition to equality/NA-ness
    res_type = type(result_fill_value)
    ex_type = type(expected_fill_value)

    if hasattr(result_fill_value, "dtype"):
        # Compare types in a way that is robust to platform-specific
        #  idiosyncrasies where e.g. sometimes we get "ulonglong" as an alias
        #  for "uint64" or "intc" as an alias for "int32"
        assert result_fill_value.dtype.kind == expected_fill_value.dtype.kind
        assert result_fill_value.dtype.itemsize == expected_fill_value.dtype.itemsize
    else:
        # On some builds, type comparison fails, e.g. np.int32 != np.int32
        assert res_type == ex_type or res_type.__name__ == ex_type.__name__

    match_value = result_fill_value == expected_fill_value
    if match_value is pd.NA:
        match_value = False

    # Note: type check above ensures that we have the _same_ NA value
    # for missing values, None == None (which is checked
    # through match_value above), but np.nan != np.nan and pd.NaT != pd.NaT
    match_missing = isna(result_fill_value) and isna(expected_fill_value)

    assert match_value or match_missing

