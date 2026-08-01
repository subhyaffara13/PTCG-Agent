
def test_validation_len_levels_matches_args():
    with pytest.raises(ValueError, match='number of input sequences'):
        crosstab([0, 1, 1], [8, 8, 9], levels=([0, 1, 2, 3],))

