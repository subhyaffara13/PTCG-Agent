
def test_empty_with_dup_column_pass_dtype_by_indexes_raises(all_parsers):
    # see gh-9424
    parser = all_parsers
    expected = concat(
        [Series([], name="one", dtype="u1"), Series([], name="one.1", dtype="f")],
        axis=1,
    )
    expected.index = expected.index.astype(object)

    with pytest.raises(ValueError, match="Duplicate names"):
        parser.read_csv(StringIO(""), names=["one", "one"], dtype={0: "u1", 1: "f"})

