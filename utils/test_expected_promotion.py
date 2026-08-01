
def test_expected_promotion(expected, dtypes, optional_dtypes, data):
    # Sample randomly while ensuring "dtypes" is always present:
    optional = data.draw(strategies.lists(
            strategies.sampled_from(dtypes + optional_dtypes)))
    all_dtypes = dtypes + optional
    dtypes_sample = data.draw(strategies.permutations(all_dtypes))

    res = np.result_type(*dtypes_sample)
    assert res == expected

