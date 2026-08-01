
def test_qcut_list_like_labels(labels, expected):
    # GH 13318
    values = range(3)
    result = qcut(values, 3, labels=labels)
    expected = Categorical(expected, ordered=True)
    tm.assert_categorical_equal(result, expected)

