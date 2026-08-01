
def test_EqualityHashKey_callable_key():
    # Common simple hash key functions.
    EqualityHashLen = curry(EqualityHashKey, len)
    EqualityHashType = curry(EqualityHashKey, type)
    EqualityHashId = curry(EqualityHashKey, id)
    EqualityHashFirst = curry(EqualityHashKey, first)
    data1 = [[], [1], (), (1,), {}, {1: 2}]
    data2 = [[1, 2], (1, 2), (1, 3), [1, 3], [2, 1], {1: 2}]
    assert list(unique(data1*3, key=EqualityHashLen)) == data1
    assert list(unique(data2*3, key=EqualityHashLen)) == data2
    assert list(unique(data1*3, key=EqualityHashType)) == data1
    assert list(unique(data2*3, key=EqualityHashType)) == data2
    assert list(unique(data1*3, key=EqualityHashId)) == data1
    assert list(unique(data2*3, key=EqualityHashId)) == data2
    assert list(unique(data2*3, key=EqualityHashFirst)) == data2

