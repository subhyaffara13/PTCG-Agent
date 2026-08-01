
def test_sequence_partitions():
    assert list(sequence_partitions([1], 1)) == [[[1]]]
    assert list(sequence_partitions([1, 2], 1)) == [[[1, 2]]]
    assert list(sequence_partitions([1, 2], 2)) == [[[1], [2]]]
    assert list(sequence_partitions([1, 2, 3], 1)) == [[[1, 2, 3]]]
    assert list(sequence_partitions([1, 2, 3], 2)) == \
        [[[1], [2, 3]], [[1, 2], [3]]]
    assert list(sequence_partitions([1, 2, 3], 3)) == [[[1], [2], [3]]]

    # Exceptional cases
    assert list(sequence_partitions([], 0)) == []
    assert list(sequence_partitions([], 1)) == []
    assert list(sequence_partitions([1, 2], 0)) == []
    assert list(sequence_partitions([1, 2], 3)) == []

