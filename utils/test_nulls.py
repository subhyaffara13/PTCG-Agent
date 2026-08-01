
def test_nulls(idx):
    # this is really a smoke test for the methods
    # as these are adequately tested for function elsewhere

    msg = "isna is not defined for MultiIndex"
    with pytest.raises(NotImplementedError, match=msg):
        idx.isna()

