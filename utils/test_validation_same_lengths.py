
def test_validation_same_lengths():
    with pytest.raises(ValueError, match='must have the same length'):
        crosstab([1, 2], [1, 2, 3, 4])

