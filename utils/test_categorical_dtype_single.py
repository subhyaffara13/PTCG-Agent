
def test_categorical_dtype_single(all_parsers, dtype, request):
    # see gh-10153
    parser = all_parsers
    data = """a,b,c
1,a,3.4
1,a,3.4
2,b,4.5"""
    expected = DataFrame(
        {"a": [1, 1, 2], "b": Categorical(["a", "a", "b"]), "c": [3.4, 3.4, 4.5]}
    )
    if parser.engine == "pyarrow":
        mark = pytest.mark.xfail(
            strict=False,
            reason="Flaky test sometimes gives object dtype instead of Categorical",
        )
        request.applymarker(mark)

    actual = parser.read_csv(StringIO(data), dtype=dtype)
    tm.assert_frame_equal(actual, expected)

