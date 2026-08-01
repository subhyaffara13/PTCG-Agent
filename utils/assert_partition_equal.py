
def assert_partition_equal(x, y):
    assert set(map(frozenset, x)) == set(map(frozenset, y))

