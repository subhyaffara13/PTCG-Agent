
def test_EqualityHashKey_index_key():
    d1 = {'firstname': 'Alice', 'age': 21, 'data': {}}
    d2 = {'firstname': 'Alice', 'age': 34, 'data': {}}
    d3a = {'firstname': 'Bob', 'age': 56, 'data': {}}
    d3b = {'firstname': 'Bob', 'age': 56, 'data': {}}
    EqualityHashFirstname = curry(EqualityHashKey, 'firstname')
    assert list(unique(3*[d1, d2, d3a, d3b],
                       key=EqualityHashFirstname)) == [d1, d2, d3a]
    EqualityHashFirstnameAge = curry(EqualityHashKey, ['firstname', 'age'])
    assert list(unique(3*[d1, d2, d3a, d3b],
                       key=EqualityHashFirstnameAge)) == [d1, d2, d3a]
    list1 = [0] * 10
    list2 = [0] * 100
    list3a = [1] * 10
    list3b = [1] * 10
    EqualityHash0 = curry(EqualityHashKey, 0)
    assert list(unique(3*[list1, list2, list3a, list3b],
                       key=EqualityHash0)) == [list1, list2, list3a]

