
def test_replace_inplace_reference_no_op(to_replace):
    df = DataFrame({"a": [1.5, 2, 3]})
    arr_a = get_array(df, "a")
    view = df[:]
    df.replace(to_replace=to_replace, value=15.5, inplace=True)

    assert np.shares_memory(get_array(df, "a"), arr_a)
    assert not df._mgr._has_no_reference(0)
    assert not view._mgr._has_no_reference(0)

