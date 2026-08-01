
def test_partition_all():
    assert list(partition_all(2, [1, 2, 3, 4])) == [(1, 2), (3, 4)]
    assert list(partition_all(3, range(5))) == [(0, 1, 2), (3, 4)]
    assert list(partition_all(2, [])) == []

    # Regression test: https://github.com/pytoolz/toolz/issues/387
    class NoCompare:
        def __eq__(self, other):
            if self.__class__ == other.__class__:
                return True
            raise ValueError()
    obj = NoCompare()
    result = [(obj, obj, obj, obj), (obj, obj, obj)]
    assert list(partition_all(4, [obj]*7)) == result
    assert list(partition_all(4, iter([obj]*7))) == result

    # Test invalid __len__: https://github.com/pytoolz/toolz/issues/602
    class ListWithBadLength(list):
        def __init__(self, contents, off_by=1):
            self.off_by = off_by
            super().__init__(contents)

        def __len__(self):
            return super().__len__() + self.off_by

    too_long_list = ListWithBadLength([1, 2], off_by=+1)
    assert raises(LookupError, lambda: list(partition_all(5, too_long_list)))
    too_short_list = ListWithBadLength([1, 2], off_by=-1)
    assert raises(LookupError, lambda: list(partition_all(5, too_short_list)))

