
def test_cossin_error_missing_partitioning():
    with pytest.raises(ValueError, match=".*exactly four arrays.* got 2"):
        cossin(unitary_group.rvs(2))

    with pytest.raises(ValueError, match=".*might be due to missing p, q"):
        cossin(unitary_group.rvs(4))

