
def test_step_not_implemented_for_cov_corr(agg):
    # GH 15354
    roll = DataFrame(range(2)).rolling(1, step=2)
    with pytest.raises(NotImplementedError, match="step not implemented"):
        getattr(roll, agg)()

