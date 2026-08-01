
def test_map_str(data, categories, ordered):
    # GH 31202 - override base class since we want to maintain categorical/ordered
    index = CategoricalIndex(data, categories=categories, ordered=ordered)
    result = index.map(str)
    expected = CategoricalIndex(
        map(str, data), categories=map(str, categories), ordered=ordered
    )
    tm.assert_index_equal(result, expected)


def test_map_str():
    # GH 2786
    df = DataFrame(np.random.default_rng(2).random((3, 4)))
    df2 = df.copy()
    cols = ["a", "a", "a", "a"]
    df.columns = cols

    expected = df2.map(str)
    expected.columns = cols
    result = df.map(str)
    tm.assert_frame_equal(result, expected)


def test_map_str(data, categories, ordered, na_action):
    # GH 31202 - override base class since we want to maintain categorical/ordered
    cat = Categorical(data, categories=categories, ordered=ordered)
    result = cat.map(str, na_action=na_action)
    expected = Categorical(
        map(str, data), categories=map(str, categories), ordered=ordered
    )
    tm.assert_categorical_equal(result, expected)

