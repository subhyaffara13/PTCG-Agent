
def test_none_to_nan(cls, dtype):
    a = cls._from_sequence(["a", None, "b"], dtype=dtype)
    assert a[1] is not None
    assert a[1] is a.dtype.na_value

