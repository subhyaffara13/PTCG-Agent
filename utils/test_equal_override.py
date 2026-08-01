
def test_equal_override():
    # gh-9153: ndarray.__eq__ uses special logic for structured arrays, which
    # did not respect overrides with __array_priority__ or __array_ufunc__.
    # The PR fixed this for __array_priority__ and __array_ufunc__ = None.
    class MyAlwaysEqual:
        def __eq__(self, other):
            return "eq"

        def __ne__(self, other):
            return "ne"

    class MyAlwaysEqualOld(MyAlwaysEqual):
        __array_priority__ = 10000

    class MyAlwaysEqualNew(MyAlwaysEqual):
        __array_ufunc__ = None

    array = np.array([(0, 1), (2, 3)], dtype='i4,i4')
    for my_always_equal_cls in MyAlwaysEqualOld, MyAlwaysEqualNew:
        my_always_equal = my_always_equal_cls()
        assert_equal(my_always_equal == array, 'eq')
        assert_equal(array == my_always_equal, 'eq')
        assert_equal(my_always_equal != array, 'ne')
        assert_equal(array != my_always_equal, 'ne')

