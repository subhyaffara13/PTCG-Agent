
def test_scalar_raises():
    with pytest.raises(ValueError, match="Cannot pass scalar '1'"):
        pd.array(1)

