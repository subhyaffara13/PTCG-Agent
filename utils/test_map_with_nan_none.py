
def test_map_with_nan_none(data, f, expected):  # GH 24241
    values = CategoricalIndex(data)
    result = values.map(f, na_action=None)
    tm.assert_index_equal(result, expected)


def test_map_with_nan_none(data, f, expected):  # GH 24241
    values = Categorical(data)
    result = values.map(f, na_action=None)
    if isinstance(expected, Categorical):
        tm.assert_categorical_equal(result, expected)
    else:
        tm.assert_index_equal(result, expected)

