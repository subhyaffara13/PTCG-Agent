
def test_is_hashable():
    # all new-style classes are hashable by default
    class HashableClass:
        pass

    class UnhashableClass1:
        __hash__ = None

    class UnhashableClass2:
        def __hash__(self):
            raise TypeError("Not hashable")

    # Temporary helper for Python 3.11 compatibility.
    # This can be removed once support for Python 3.11 is dropped.
    class HashableSlice:
        def __init__(self, start, stop, step=None):
            self.slice = slice(start, stop, step)

        def __eq__(self, other):
            return isinstance(other, HashableSlice) and self.slice == other.slice

        def __hash__(self):
            return hash((self.slice.start, self.slice.stop, self.slice.step))

        def __repr__(self):
            return (
                f"HashableSlice({self.slice.start}, {self.slice.stop}, "
                f"{self.slice.step})"
            )

    hashable = (1, 3.14, np.float64(3.14), "a", (), (1,), HashableClass())
    not_hashable = ([], UnhashableClass1())
    abc_hashable_not_really_hashable = (([],), UnhashableClass2())
    hashable_slice = HashableSlice(1, 2)
    tuple_with_slice = (slice(1, 2), 3)

    for i in hashable:
        assert inference.is_hashable(i)
        assert inference.is_hashable(i, allow_slice=True)
        assert inference.is_hashable(i, allow_slice=False)
    for i in not_hashable:
        assert not inference.is_hashable(i)
        assert not inference.is_hashable(i, allow_slice=True)
        assert not inference.is_hashable(i, allow_slice=False)
    for i in abc_hashable_not_really_hashable:
        assert not inference.is_hashable(i)
        assert not inference.is_hashable(i, allow_slice=True)
        assert not inference.is_hashable(i, allow_slice=False)

    assert inference.is_hashable(hashable_slice)
    assert inference.is_hashable(hashable_slice, allow_slice=True)
    assert inference.is_hashable(hashable_slice, allow_slice=False)

    if PY312:
        for obj in [slice(1, 2), tuple_with_slice]:
            assert inference.is_hashable(obj)
            assert inference.is_hashable(obj, allow_slice=True)
            assert not inference.is_hashable(obj, allow_slice=False)
    else:
        for obj in [slice(1, 2), tuple_with_slice]:
            assert not inference.is_hashable(obj)
            assert not inference.is_hashable(obj, allow_slice=True)
            assert not inference.is_hashable(obj, allow_slice=False)

    # numpy.array is no longer collections.abc.Hashable as of
    # https://github.com/numpy/numpy/pull/5326, just test
    # is_hashable()
    assert not inference.is_hashable(np.array([]))

