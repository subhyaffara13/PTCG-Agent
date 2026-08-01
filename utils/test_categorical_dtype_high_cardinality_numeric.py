
def test_categorical_dtype_high_cardinality_numeric(all_parsers, monkeypatch):
    # see gh-18186
    # was an issue with C parser, due to DEFAULT_BUFFER_HEURISTIC
    parser = all_parsers
    heuristic = 2**5
    data = np.sort([str(i) for i in range(heuristic + 1)])
    expected = DataFrame({"a": Categorical(data, ordered=True)})
    with monkeypatch.context() as m:
        m.setattr(libparsers, "DEFAULT_BUFFER_HEURISTIC", heuristic)
        actual = parser.read_csv(StringIO("a\n" + "\n".join(data)), dtype="category")
    actual["a"] = actual["a"].cat.reorder_categories(
        np.sort(actual.a.cat.categories), ordered=True
    )
    tm.assert_frame_equal(actual, expected)

