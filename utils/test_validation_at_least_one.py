
def test_validation_at_least_one():
    with pytest.raises(TypeError, match='At least one'):
        crosstab()

