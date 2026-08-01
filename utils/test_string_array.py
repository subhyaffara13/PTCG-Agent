
def test_string_array():
    arr = m.create_string_array(True)
    assert str(arr.dtype) == "[('a', 'S3'), ('b', 'S3')]"
    assert m.print_string_array(arr) == [
        "a='',b=''",
        "a='a',b='a'",
        "a='ab',b='ab'",
        "a='abc',b='abc'",
    ]
    dtype = arr.dtype
    assert arr["a"].tolist() == [b"", b"a", b"ab", b"abc"]
    assert arr["b"].tolist() == [b"", b"a", b"ab", b"abc"]
    arr = m.create_string_array(False)
    assert dtype == arr.dtype


def test_string_array(nullable_string_dtype, any_string_method):
    method_name, args, kwargs = any_string_method

    data = ["a", "bb", np.nan, "ccc"]
    a = Series(data, dtype=object)
    b = Series(data, dtype=nullable_string_dtype)

    if method_name == "decode":
        with pytest.raises(TypeError, match="a bytes-like object is required"):
            getattr(b.str, method_name)(*args, **kwargs)
        return

    expected = getattr(a.str, method_name)(*args, **kwargs)
    result = getattr(b.str, method_name)(*args, **kwargs)

    if isinstance(expected, Series):
        if expected.dtype == "object" and lib.is_string_array(
            expected.dropna().values,
        ):
            assert result.dtype == nullable_string_dtype
            result = result.astype(object)

        elif expected.dtype == "object" and lib.is_bool_array(
            expected.values, skipna=True
        ):
            assert result.dtype == "boolean"
            expected = expected.astype("boolean")

        elif expected.dtype == "bool":
            assert result.dtype == "boolean"
            result = result.astype("bool")

        elif expected.dtype == "float" and expected.isna().any():
            assert result.dtype == "Int64"
            result = result.astype("float")

        if expected.dtype == object:
            # GH#18463
            expected[expected.isna()] = NA

    elif isinstance(expected, DataFrame):
        columns = expected.select_dtypes(include="object").columns
        assert all(result[columns].dtypes == nullable_string_dtype)
        result[columns] = result[columns].astype(object)
        expected[columns] = expected[columns].fillna(NA)  # GH#18463

    tm.assert_equal(result, expected)

