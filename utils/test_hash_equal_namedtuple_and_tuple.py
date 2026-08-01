
def test_hash_equal_namedtuple_and_tuple():
    T = namedtuple("T", ["x", "y"])
    a = T(1, (2, 3))
    b = (1, (2, 3))
    assert ht.object_hash(a) == ht.object_hash(b)
    assert ht.objects_are_equal(a, b)

