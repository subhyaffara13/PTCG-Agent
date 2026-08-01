
def test_hash_collisions():
    # Hash collisions are bad.
    #
    # https://github.com/pandas-dev/pandas/issues/14711#issuecomment-264885726
    hashes = [
        "Ingrid-9Z9fKIZmkO7i7Cn51Li34pJm44fgX6DYGBNj3VPlOH50m7HnBlPxfIwFMrcNJNMP6PSgLmwWnInciMWrCSAlLEvt7JkJl4IxiMrVbXSa8ZQoVaq5xoQPjltuJEfwdNlO6jo8qRRHvD8sBEBMQASrRa6TsdaPTPCBo3nwIBpE7YzzmyH0vMBhjQZLx1aCT7faSEx7PgFxQhHdKFWROcysamgy9iVj8DO2Fmwg1NNl93rIAqC3mdqfrCxrzfvIY8aJdzin2cHVzy3QUJxZgHvtUtOLxoqnUHsYbNTeq0xcLXpTZEZCxD4PGubIuCNf32c33M7HFsnjWSEjE2yVdWKhmSVodyF8hFYVmhYnMCztQnJrt3O8ZvVRXd5IKwlLexiSp4h888w7SzAIcKgc3g5XQJf6MlSMftDXm9lIsE1mJNiJEv6uY6pgvC3fUPhatlR5JPpVAHNSbSEE73MBzJrhCAbOLXQumyOXigZuPoME7QgJcBalliQol7YZ9",
        "Tim-b9MddTxOWW2AT1Py6vtVbZwGAmYCjbp89p8mxsiFoVX4FyDOF3wFiAkyQTUgwg9sVqVYOZo09Dh1AzhFHbgij52ylF0SEwgzjzHH8TGY8Lypart4p4onnDoDvVMBa0kdthVGKl6K0BDVGzyOXPXKpmnMF1H6rJzqHJ0HywfwS4XYpVwlAkoeNsiicHkJUFdUAhG229INzvIAiJuAHeJDUoyO4DCBqtoZ5TDend6TK7Y914yHlfH3g1WZu5LksKv68VQHJriWFYusW5e6ZZ6dKaMjTwEGuRgdT66iU5nqWTHRH8WSzpXoCFwGcTOwyuqPSe0fTe21DVtJn1FKj9F9nEnR9xOvJUO7E0piCIF4Ad9yAIDY4DBimpsTfKXCu1vdHpKYerzbndfuFe5AhfMduLYZJi5iAw8qKSwR5h86ttXV0Mc0QmXz8dsRvDgxjXSmupPxBggdlqUlC828hXiTPD7am0yETBV0F3bEtvPiNJfremszcV8NcqAoARMe",
    ]

    # These should be different.
    result1 = hash_array(np.asarray(hashes[0:1], dtype=object), "utf8")
    expected1 = np.array([14963968704024874985], dtype=np.uint64)
    tm.assert_numpy_array_equal(result1, expected1)

    result2 = hash_array(np.asarray(hashes[1:2], dtype=object), "utf8")
    expected2 = np.array([16428432627716348016], dtype=np.uint64)
    tm.assert_numpy_array_equal(result2, expected2)

    result = hash_array(np.asarray(hashes, dtype=object), "utf8")
    tm.assert_numpy_array_equal(result, np.concatenate([expected1, expected2], axis=0))


def test_hash_collisions(monkeypatch):
    # non-smoke test that we don't get hash collisions
    size_cutoff = 50
    with monkeypatch.context() as m:
        m.setattr(libindex, "_SIZE_CUTOFF", size_cutoff)
        index = MultiIndex.from_product(
            [np.arange(8), np.arange(8)], names=["one", "two"]
        )
        result = index.get_indexer(index.values)
        tm.assert_numpy_array_equal(result, np.arange(len(index), dtype="intp"))

        for i in [0, 1, len(index) - 2, len(index) - 1]:
            result = index.get_loc(index[i])
            assert result == i

