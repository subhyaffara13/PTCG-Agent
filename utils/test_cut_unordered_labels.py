
def test_cut_unordered_labels(data, bins, labels, expected_codes, expected_labels):
    # GH 33141
    result = cut(data, bins=bins, labels=labels, ordered=False)
    expected = Categorical.from_codes(
        expected_codes, categories=expected_labels, ordered=False
    )
    tm.assert_categorical_equal(result, expected)

