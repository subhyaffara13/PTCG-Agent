
def test_is_list_like_iter_is_none():
    # GH 43373
    # is_list_like was yielding false positives with __iter__ == None
    class NotListLike:
        def __getitem__(self, item):
            return self

        __iter__ = None

    assert not inference.is_list_like(NotListLike())

