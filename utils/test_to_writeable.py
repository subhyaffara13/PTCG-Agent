
def test_to_writeable():
    # Test to_writeable function
    res = to_writeable(np.array([1]))  # pass through ndarrays
    assert_equal(res.shape, (1,))
    assert_array_equal(res, 1)
    # Dict fields can be written in any order
    expected1 = np.array([(1, 2)], dtype=[('a', '|O8'), ('b', '|O8')])
    expected2 = np.array([(2, 1)], dtype=[('b', '|O8'), ('a', '|O8')])
    alternatives = (expected1, expected2)
    assert_any_equal(to_writeable({'a':1,'b':2}), alternatives)
    # Fields with underscores discarded with a warning message.
    with pytest.warns(MatWriteWarning, match='Starting field name with'):
        assert_any_equal(to_writeable({'a':1, 'b':2, '_c':3}), alternatives)
    # Not-string fields discarded
    assert_any_equal(to_writeable({'a':1,'b':2, 100:3}), alternatives)
    # String fields that are valid Python identifiers discarded
    with pytest.warns(MatWriteWarning, match='Starting field name with'):
        assert_any_equal(to_writeable({'a':1, 'b':2, '99':3}), alternatives)
    # Object with field names is equivalent

    class klass:
        pass

    c = klass
    c.a = 1
    c.b = 2
    assert_any_equal(to_writeable(c), alternatives)
    # empty list and tuple go to empty array
    res = to_writeable([])
    assert_equal(res.shape, (0,))
    assert_equal(res.dtype.type, np.float64)
    res = to_writeable(())
    assert_equal(res.shape, (0,))
    assert_equal(res.dtype.type, np.float64)
    # None -> None
    assert_(to_writeable(None) is None)
    # String to strings
    assert_equal(to_writeable('a string').dtype.type, np.str_)
    # Scalars to numpy to NumPy scalars
    res = to_writeable(1)
    assert_equal(res.shape, ())
    assert_equal(res.dtype.type, np.array(1).dtype.type)
    assert_array_equal(res, 1)
    # Empty dict returns EmptyStructMarker
    assert_(to_writeable({}) is EmptyStructMarker)
    # Object does not have (even empty) __dict__
    assert_(to_writeable(object()) is None)
    # Custom object does have empty __dict__, returns EmptyStructMarker

    class C:
        pass

    assert_(to_writeable(c()) is EmptyStructMarker)
    # dict keys with legal characters are convertible
    res = to_writeable({'a': 1})['a']
    assert_equal(res.shape, (1,))
    assert_equal(res.dtype.type, np.object_)
    # Only fields with illegal characters, falls back to EmptyStruct
    with pytest.warns(MatWriteWarning, match='Starting field name with'):
        assert_(to_writeable({'1':1}) is EmptyStructMarker)

    with pytest.warns(MatWriteWarning, match='Starting field name with'):
        assert_(to_writeable({'_a':1}) is EmptyStructMarker)
    # Unless there are valid fields, in which case structured array
    with pytest.warns(MatWriteWarning, match='Starting field name with'):
        assert_equal(to_writeable({'1':1, 'f': 2}),
                 np.array([(2,)], dtype=[('f', '|O8')]))

