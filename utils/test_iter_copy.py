
def test_iter_copy():
    # Check that copying the iterator works correctly
    a = arange(24).reshape(2, 3, 4)

    # Simple iterator
    i = nditer(a)
    j = i.copy()
    assert_equal([x[()] for x in i], [x[()] for x in j])

    i.iterindex = 3
    j = i.copy()
    assert_equal([x[()] for x in i], [x[()] for x in j])

    # Buffered iterator
    i = nditer(a, ['buffered', 'ranged'], order='F', buffersize=3)
    j = i.copy()
    assert_equal([x[()] for x in i], [x[()] for x in j])

    i.iterindex = 3
    j = i.copy()
    assert_equal([x[()] for x in i], [x[()] for x in j])

    i.iterrange = (3, 9)
    j = i.copy()
    assert_equal([x[()] for x in i], [x[()] for x in j])

    i.iterrange = (2, 18)
    next(i)
    next(i)
    j = i.copy()
    assert_equal([x[()] for x in i], [x[()] for x in j])

    # Casting iterator
    with nditer(a, ['buffered'], order='F', casting='unsafe',
                op_dtypes='f8', buffersize=5) as i:
        j = i.copy()
    assert_equal([x[()] for x in j], a.ravel(order='F'))

    a = arange(24, dtype='<i4').reshape(2, 3, 4)
    with nditer(a, ['buffered'], order='F', casting='unsafe',
                op_dtypes='>f8', buffersize=5) as i:
        j = i.copy()
    assert_equal([x[()] for x in j], a.ravel(order='F'))

