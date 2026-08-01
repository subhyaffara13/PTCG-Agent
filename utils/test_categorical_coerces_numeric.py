
def test_categorical_coerces_numeric(all_parsers):
    parser = all_parsers
    dtype = {"b": CategoricalDtype([1, 2, 3])}

    data = "b\n1\n1\n2\n3"
    expected = DataFrame({"b": Categorical([1, 1, 2, 3])})

    result = parser.read_csv(StringIO(data), dtype=dtype)
    tm.assert_frame_equal(result, expected)

