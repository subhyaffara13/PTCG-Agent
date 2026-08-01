
def test_chunked_categorical(version, temp_file):
    df = DataFrame({"cats": Series(["a", "b", "a", "b", "c"], dtype="category")})
    df.index.name = "index"

    expected = df.copy()

    df.to_stata(temp_file, version=version)
    with StataReader(temp_file, chunksize=2, order_categoricals=False) as reader:
        for i, block in enumerate(reader):
            block = block.set_index("index")
            assert "cats" in block
            tm.assert_series_equal(
                block.cats,
                expected.cats.iloc[2 * i : 2 * (i + 1)],
                check_index_type=len(block) > 1,
            )

