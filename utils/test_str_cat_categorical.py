
def test_str_cat_categorical(
    index_or_series, dtype_caller, dtype_target, sep, infer_string
):
    box = index_or_series

    with option_context("future.infer_string", infer_string):
        s = Index(["a", "a", "b", "a"], dtype=dtype_caller)
        s = s if box == Index else Series(s, index=s, dtype=s.dtype)
        t = Index(["b", "a", "b", "c"], dtype=dtype_target)

        expected = Index(
            ["ab", "aa", "bb", "ac"], dtype=object if dtype_caller == "object" else None
        )
        expected = (
            expected
            if box == Index
            else Series(
                expected, index=Index(s, dtype=dtype_caller), dtype=expected.dtype
            )
        )

        # Series/Index with unaligned Index -> t.values
        result = s.str.cat(t.values, sep=sep)
        tm.assert_equal(result, expected)

        # Series/Index with Series having matching Index
        t = Series(t.values, index=Index(s, dtype=dtype_caller))
        result = s.str.cat(t, sep=sep)
        tm.assert_equal(result, expected)

        # Series/Index with Series.values
        result = s.str.cat(t.values, sep=sep)
        tm.assert_equal(result, expected)

        # Series/Index with Series having different Index
        t = Series(t.values, index=t.values)
        expected = Index(
            ["aa", "aa", "bb", "bb", "aa"],
            dtype=object if dtype_caller == "object" else None,
        )
        dtype = object if dtype_caller == "object" else s.dtype.categories.dtype
        expected = (
            expected
            if box == Index
            else Series(
                expected,
                index=Index(expected.str[:1], dtype=dtype),
                dtype=expected.dtype,
            )
        )

        result = s.str.cat(t, sep=sep)
        tm.assert_equal(result, expected)

