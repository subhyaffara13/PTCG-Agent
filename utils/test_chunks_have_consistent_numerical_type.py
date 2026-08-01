
def test_chunks_have_consistent_numerical_type(all_parsers, monkeypatch):
    # mainly an issue with the C parser
    heuristic = 2**3
    parser = all_parsers
    integers = [str(i) for i in range(heuristic - 1)]
    data = "a\n" + "\n".join([*integers, "1.0", "2.0", *integers])

    # Coercions should work without warnings.
    with monkeypatch.context() as m:
        m.setattr(libparsers, "DEFAULT_BUFFER_HEURISTIC", heuristic)
        result = parser.read_csv(StringIO(data))

    assert type(result.a[0]) is np.float64
    assert result.a.dtype == float

