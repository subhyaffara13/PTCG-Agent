
def test_unstack_single_index_series():
    # GH 36113
    msg = r"index must be a MultiIndex to unstack.*"
    with pytest.raises(ValueError, match=msg):
        Series(dtype=np.int64).unstack()

