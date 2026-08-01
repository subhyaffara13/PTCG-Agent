
def test_unzip():
    def _to_lists(seq, n=10):
        """iter of iters -> finite list of finite lists
        """
        def initial(s):
            return list(take(n, s))

        return initial(map(initial, seq))

    def _assert_initial_matches(a, b, n=10):
        assert list(take(n, a)) == list(take(n, b))

    # Unzips a simple list correctly
    assert _to_lists(unzip([('a', 1), ('b', 2), ('c', 3)])) \
        == [['a', 'b', 'c'], [1, 2, 3]]

    # Can handle a finite number of infinite iterators (the naive unzip
    # implementation `zip(*args)` implementation fails on this example).
    a, b, c = unzip(zip(count(1), repeat(0), repeat(1)))
    _assert_initial_matches(a, count(1))
    _assert_initial_matches(b, repeat(0))
    _assert_initial_matches(c, repeat(1))

    # Sensibly handles empty input
    assert list(unzip(zip([]))) == []

