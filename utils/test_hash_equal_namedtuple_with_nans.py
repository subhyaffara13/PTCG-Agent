
def test_hash_equal_namedtuple_with_nans():
    T = namedtuple("T", ["x", "y"])
    a = T(float("nan"), (float("nan"), float("nan")))
    b = T(float("nan"), (float("nan"), float("nan")))
    assert ht.object_hash(a) == ht.object_hash(b)
    assert ht.objects_are_equal(a, b)

