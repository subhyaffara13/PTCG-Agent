
def test_map_with_dict_or_series():
    orig_values = ["a", "B", 1, "a"]
    new_values = ["one", 2, 3.0, "one"]
    cur_index = CategoricalIndex(orig_values, name="XXX")
    expected = CategoricalIndex(new_values, name="XXX", categories=[3.0, 2, "one"])

    mapper = Series(new_values[:-1], index=orig_values[:-1])
    result = cur_index.map(mapper)
    # Order of categories in result can be different
    tm.assert_index_equal(result, expected)

    mapper = dict(zip(orig_values[:-1], new_values[:-1]))
    result = cur_index.map(mapper)
    # Order of categories in result can be different
    tm.assert_index_equal(result, expected)


def test_map_with_dict_or_series(na_action):
    orig_values = ["a", "B", 1, "a"]
    new_values = ["one", 2, 3.0, "one"]
    cat = Categorical(orig_values)

    mapper = Series(new_values[:-1], index=orig_values[:-1])
    result = cat.map(mapper, na_action=na_action)

    # Order of categories in result can be different
    expected = Categorical(new_values, categories=[3.0, 2, "one"])
    tm.assert_categorical_equal(result, expected)

    mapper = dict(zip(orig_values[:-1], new_values[:-1], strict=True))
    result = cat.map(mapper, na_action=na_action)
    # Order of categories in result can be different
    tm.assert_categorical_equal(result, expected)

