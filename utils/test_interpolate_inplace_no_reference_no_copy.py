
def test_interpolate_inplace_no_reference_no_copy(vals):
    df = DataFrame({"a": vals})
    arr = get_array(df, "a")
    df.interpolate(method="linear", inplace=True)

    assert np.shares_memory(arr, get_array(df, "a"))
    # Check that we don't have references when triggering a copy
    assert df._mgr._has_no_reference(0)

