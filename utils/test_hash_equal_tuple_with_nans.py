
def test_hash_equal_tuple_with_nans():
    a = (float("nan"), (float("nan"), float("nan")))
    b = (float("nan"), (float("nan"), float("nan")))
    assert ht.object_hash(a) == ht.object_hash(b)
    assert ht.objects_are_equal(a, b)

