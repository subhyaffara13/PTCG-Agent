
def test_bxp_bad_positions():
    with pytest.raises(ValueError):
        _bxp_test_helper(bxp_kwargs=dict(positions=[2, 3]))

