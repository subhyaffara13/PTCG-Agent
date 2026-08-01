
def compare_element(result, expected, typ):
    if isinstance(expected, Index):
        tm.assert_index_equal(result, expected)
        return

    if typ.startswith("sp_"):
        tm.assert_equal(result, expected)
    elif typ == "timestamp":
        if expected is pd.NaT:
            assert result is pd.NaT
        else:
            assert result == expected
    else:
        comparator = getattr(tm, f"assert_{typ}_equal", tm.assert_almost_equal)
        comparator(result, expected)

