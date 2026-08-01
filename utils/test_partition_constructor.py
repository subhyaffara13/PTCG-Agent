
def test_partition_constructor():
    raises(ValueError, lambda: Partition([1, 1, 2]))
    raises(ValueError, lambda: Partition([1, 2, 3], [2, 3, 4]))
    raises(ValueError, lambda: Partition(1, 2, 3))
    raises(ValueError, lambda: Partition(*list(range(3))))

    assert Partition([1, 2, 3], [4, 5]) == Partition([4, 5], [1, 2, 3])
    assert Partition({1, 2, 3}, {4, 5}) == Partition([1, 2, 3], [4, 5])

    a = FiniteSet(1, 2, 3)
    b = FiniteSet(4, 5)
    assert Partition(a, b) == Partition([1, 2, 3], [4, 5])
    assert Partition({a, b}) == Partition(FiniteSet(a, b))
    assert Partition({a, b}) != Partition(a, b)

