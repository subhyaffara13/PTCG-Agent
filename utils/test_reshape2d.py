
def test_reshape2d():

    class Dummy:
        pass

    xnew = cbook._reshape_2D([], 'x')
    assert np.shape(xnew) == (1, 0)

    x = [Dummy() for _ in range(5)]

    xnew = cbook._reshape_2D(x, 'x')
    assert np.shape(xnew) == (1, 5)

    x = np.arange(5)
    xnew = cbook._reshape_2D(x, 'x')
    assert np.shape(xnew) == (1, 5)

    x = [[Dummy() for _ in range(5)] for _ in range(3)]
    xnew = cbook._reshape_2D(x, 'x')
    assert np.shape(xnew) == (3, 5)

    # this is strange behaviour, but...
    x = np.random.rand(3, 5)
    xnew = cbook._reshape_2D(x, 'x')
    assert np.shape(xnew) == (5, 3)

    # Test a list of lists which are all of length 1
    x = [[1], [2], [3]]
    xnew = cbook._reshape_2D(x, 'x')
    assert isinstance(xnew, list)
    assert isinstance(xnew[0], np.ndarray) and xnew[0].shape == (1,)
    assert isinstance(xnew[1], np.ndarray) and xnew[1].shape == (1,)
    assert isinstance(xnew[2], np.ndarray) and xnew[2].shape == (1,)

    # Test a list of zero-dimensional arrays
    x = [np.array(0), np.array(1), np.array(2)]
    xnew = cbook._reshape_2D(x, 'x')
    assert isinstance(xnew, list)
    assert len(xnew) == 1
    assert isinstance(xnew[0], np.ndarray) and xnew[0].shape == (3,)

    # Now test with a list of lists with different lengths, which means the
    # array will internally be converted to a 1D object array of lists
    x = [[1, 2, 3], [3, 4], [2]]
    xnew = cbook._reshape_2D(x, 'x')
    assert isinstance(xnew, list)
    assert isinstance(xnew[0], np.ndarray) and xnew[0].shape == (3,)
    assert isinstance(xnew[1], np.ndarray) and xnew[1].shape == (2,)
    assert isinstance(xnew[2], np.ndarray) and xnew[2].shape == (1,)

    # We now need to make sure that this works correctly for Numpy subclasses
    # where iterating over items can return subclasses too, which may be
    # iterable even if they are scalars. To emulate this, we make a Numpy
    # array subclass that returns Numpy 'scalars' when iterating or accessing
    # values, and these are technically iterable if checking for example
    # isinstance(x, collections.abc.Iterable).

    class ArraySubclass(np.ndarray):

        def __iter__(self):
            for value in super().__iter__():
                yield np.array(value)

        def __getitem__(self, item):
            return np.array(super().__getitem__(item))

    v = np.arange(10, dtype=float)
    x = ArraySubclass((10,), dtype=float, buffer=v.data)

    xnew = cbook._reshape_2D(x, 'x')

    # We check here that the array wasn't split up into many individual
    # ArraySubclass, which is what used to happen due to a bug in _reshape_2D
    assert len(xnew) == 1
    assert isinstance(xnew[0], ArraySubclass)

    # check list of strings:
    x = ['a', 'b', 'c', 'c', 'dd', 'e', 'f', 'ff', 'f']
    xnew = cbook._reshape_2D(x, 'x')
    assert len(xnew[0]) == len(x)
    assert isinstance(xnew[0], np.ndarray)

