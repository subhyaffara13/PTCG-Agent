
def test_dtype_and_names_error(c_parser_only):
    # see gh-8833: passing both dtype and names
    # resulting in an error reporting issue
    parser = c_parser_only
    data = """
1.0 1
2.0 2
3.0 3
"""
    # base cases
    result = parser.read_csv(StringIO(data), sep=r"\s+", header=None)
    expected = DataFrame([[1.0, 1], [2.0, 2], [3.0, 3]])
    tm.assert_frame_equal(result, expected)

    result = parser.read_csv(StringIO(data), sep=r"\s+", header=None, names=["a", "b"])
    expected = DataFrame([[1.0, 1], [2.0, 2], [3.0, 3]], columns=["a", "b"])
    tm.assert_frame_equal(result, expected)

    # fallback casting
    result = parser.read_csv(
        StringIO(data), sep=r"\s+", header=None, names=["a", "b"], dtype={"a": np.int32}
    )
    expected = DataFrame([[1, 1], [2, 2], [3, 3]], columns=["a", "b"])
    expected["a"] = expected["a"].astype(np.int32)
    tm.assert_frame_equal(result, expected)

    data = """
1.0 1
nan 2
3.0 3
"""
    # fallback casting, but not castable
    if not WASM:  # no fp exception support in wasm
        with pytest.raises(ValueError, match="cannot safely convert"):
            with tm.assert_produces_warning(RuntimeWarning, check_stacklevel=False):
                parser.read_csv(
                    StringIO(data),
                    sep=r"\s+",
                    header=None,
                    names=["a", "b"],
                    dtype={"a": np.int32},
                )

