
def test_interpolate_triggers_copy(vals, func):
    df = DataFrame({"a": vals})
    result = getattr(df, func)()

    assert not np.shares_memory(get_array(result, "a"), get_array(df, "a"))
    # Check that we don't have references when triggering a copy
    assert result._mgr._has_no_reference(0)

