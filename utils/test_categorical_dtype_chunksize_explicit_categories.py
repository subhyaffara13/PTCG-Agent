
def test_categorical_dtype_chunksize_explicit_categories(all_parsers):
    # see gh-10153
    parser = all_parsers
    data = """a,b
1,a
1,b
1,b
2,c"""
    cats = ["a", "b", "c"]
    expecteds = [
        DataFrame({"a": [1, 1], "b": Categorical(["a", "b"], categories=cats)}),
        DataFrame(
            {"a": [1, 2], "b": Categorical(["b", "c"], categories=cats)},
            index=[2, 3],
        ),
    ]
    dtype = CategoricalDtype(cats)

    if parser.engine == "pyarrow":
        msg = "The 'chunksize' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), dtype={"b": dtype}, chunksize=2)
        return

    with parser.read_csv(StringIO(data), dtype={"b": dtype}, chunksize=2) as actuals:
        for actual, expected in zip(actuals, expecteds):
            tm.assert_frame_equal(actual, expected)

