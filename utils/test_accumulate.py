
def test_accumulate():
    assert list(accumulate(add, [1, 2, 3, 4, 5])) == [1, 3, 6, 10, 15]
    assert list(accumulate(mul, [1, 2, 3, 4, 5])) == [1, 2, 6, 24, 120]
    assert list(accumulate(add, [1, 2, 3, 4, 5], -1)) == [-1, 0, 2, 5, 9, 14]

    def binop(a, b):
        raise AssertionError('binop should not be called')

    start = object()
    assert list(accumulate(binop, [], start)) == [start]
    assert list(accumulate(binop, [])) == []
    assert list(accumulate(add, [1, 2, 3], no_default2)) == [1, 3, 6]

