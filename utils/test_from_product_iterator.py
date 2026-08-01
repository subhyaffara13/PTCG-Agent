
def test_from_product_iterator():
    # GH 18434
    first = ["foo", "bar", "buz"]
    second = ["a", "b", "c"]
    names = ["first", "second"]
    tuples = [
        ("foo", "a"),
        ("foo", "b"),
        ("foo", "c"),
        ("bar", "a"),
        ("bar", "b"),
        ("bar", "c"),
        ("buz", "a"),
        ("buz", "b"),
        ("buz", "c"),
    ]
    expected = MultiIndex.from_tuples(tuples, names=names)

    # iterator as input
    result = MultiIndex.from_product(iter([first, second]), names=names)
    tm.assert_index_equal(result, expected)

    # Invalid non-iterable input
    msg = "Input must be a list / sequence of iterables."
    with pytest.raises(TypeError, match=msg):
        MultiIndex.from_product(0)

