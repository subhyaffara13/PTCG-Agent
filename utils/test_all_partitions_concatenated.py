
def test_all_partitions_concatenated():
    # make sure that _all_paritions_concatenated produces the correct number
    # of partitions of the data into samples of the given sizes and that
    # all are unique
    n = np.array([3, 2, 4], dtype=int)
    nc = np.cumsum(n)

    all_partitions = set()
    counter = 0
    for partition_concatenated in _resampling._all_partitions_concatenated(n):
        counter += 1
        partitioning = np.split(partition_concatenated, nc[:-1])
        all_partitions.add(tuple([frozenset(i) for i in partitioning]))

    expected = np.prod([special.binom(sum(n[i:]), sum(n[i+1:]))
                        for i in range(len(n)-1)])

    assert_equal(counter, expected)
    assert_equal(len(all_partitions), expected)

