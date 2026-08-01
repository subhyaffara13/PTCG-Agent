
def test_categorical_dtype_coerces_boolean(all_parsers, data):
    # see gh-20498
    parser = all_parsers
    dtype = {"b": CategoricalDtype([False, True])}
    expected = DataFrame({"b": Categorical([True, False, None, False])})

    result = parser.read_csv(StringIO(data), dtype=dtype)
    tm.assert_frame_equal(result, expected)

