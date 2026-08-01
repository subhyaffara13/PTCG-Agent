
def test_modes_with_nans():
    # GH42688, nans aren't mangled
    nulls = [pd.NA, np.nan, pd.NaT, None]
    values = np.array([True] + nulls * 2, dtype=np.object_)
    modes = ht.mode(values, False)[0]
    assert modes.size == len(nulls)

