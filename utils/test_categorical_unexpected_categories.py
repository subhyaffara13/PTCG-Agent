
def test_categorical_unexpected_categories(all_parsers):
    parser = all_parsers
    dtype = {"b": CategoricalDtype(["a", "b", "d", "e"])}

    data = "b\nd\na\nc\nd"  # Unexpected c
    expected = DataFrame({"b": Categorical(["d", "a", None, "d"], dtype=dtype["b"])})

    msg = "Constructing a Categorical with a dtype and values containing"
    with tm.assert_produces_warning(Pandas4Warning, match=msg, check_stacklevel=False):
        result = parser.read_csv(StringIO(data), dtype=dtype)
    tm.assert_frame_equal(result, expected)

