
def test_vectorize():
    n = 3
    array = m.create_rec_simple(n)
    values = m.f_simple_vectorized(array)
    np.testing.assert_array_equal(values, [0, 10, 20])
    array_2 = m.f_simple_pass_thru_vectorized(array)
    np.testing.assert_array_equal(array, array_2)


def test_vectorize(capture):
    assert np.isclose(m.vectorized_func3(np.array(3 + 7j)), [6 + 14j])

    for f in [m.vectorized_func, m.vectorized_func2]:
        with capture:
            assert np.isclose(f(1, 2, 3), 6)
        assert capture == "my_func(x:int=1, y:float=2, z:float=3)"
        with capture:
            assert np.isclose(f(np.array(1), np.array(2), 3), 6)
        assert capture == "my_func(x:int=1, y:float=2, z:float=3)"
        with capture:
            assert np.allclose(f(np.array([1, 3]), np.array([2, 4]), 3), [6, 36])
        assert (
            capture
            == """
            my_func(x:int=1, y:float=2, z:float=3)
            my_func(x:int=3, y:float=4, z:float=3)
        """
        )
        with capture:
            a = np.array([[1, 2], [3, 4]], order="F")
            b = np.array([[10, 20], [30, 40]], order="F")
            c = 3
            result = f(a, b, c)
            assert np.allclose(result, a * b * c)
            assert result.flags.f_contiguous
        # All inputs are F order and full or singletons, so we the result is in col-major order:
        assert (
            capture
            == """
            my_func(x:int=1, y:float=10, z:float=3)
            my_func(x:int=3, y:float=30, z:float=3)
            my_func(x:int=2, y:float=20, z:float=3)
            my_func(x:int=4, y:float=40, z:float=3)
        """
        )
        with capture:
            a, b, c = (
                np.array([[1, 3, 5], [7, 9, 11]]),
                np.array([[2, 4, 6], [8, 10, 12]]),
                3,
            )
            assert np.allclose(f(a, b, c), a * b * c)
        assert (
            capture
            == """
            my_func(x:int=1, y:float=2, z:float=3)
            my_func(x:int=3, y:float=4, z:float=3)
            my_func(x:int=5, y:float=6, z:float=3)
            my_func(x:int=7, y:float=8, z:float=3)
            my_func(x:int=9, y:float=10, z:float=3)
            my_func(x:int=11, y:float=12, z:float=3)
        """
        )
        with capture:
            a, b, c = np.array([[1, 2, 3], [4, 5, 6]]), np.array([2, 3, 4]), 2
            assert np.allclose(f(a, b, c), a * b * c)
        assert (
            capture
            == """
            my_func(x:int=1, y:float=2, z:float=2)
            my_func(x:int=2, y:float=3, z:float=2)
            my_func(x:int=3, y:float=4, z:float=2)
            my_func(x:int=4, y:float=2, z:float=2)
            my_func(x:int=5, y:float=3, z:float=2)
            my_func(x:int=6, y:float=4, z:float=2)
        """
        )
        with capture:
            a, b, c = np.array([[1, 2, 3], [4, 5, 6]]), np.array([[2], [3]]), 2
            assert np.allclose(f(a, b, c), a * b * c)
        assert (
            capture
            == """
            my_func(x:int=1, y:float=2, z:float=2)
            my_func(x:int=2, y:float=2, z:float=2)
            my_func(x:int=3, y:float=2, z:float=2)
            my_func(x:int=4, y:float=3, z:float=2)
            my_func(x:int=5, y:float=3, z:float=2)
            my_func(x:int=6, y:float=3, z:float=2)
        """
        )
        with capture:
            a, b, c = (
                np.array([[1, 2, 3], [4, 5, 6]], order="F"),
                np.array([[2], [3]]),
                2,
            )
            assert np.allclose(f(a, b, c), a * b * c)
        assert (
            capture
            == """
            my_func(x:int=1, y:float=2, z:float=2)
            my_func(x:int=2, y:float=2, z:float=2)
            my_func(x:int=3, y:float=2, z:float=2)
            my_func(x:int=4, y:float=3, z:float=2)
            my_func(x:int=5, y:float=3, z:float=2)
            my_func(x:int=6, y:float=3, z:float=2)
        """
        )
        with capture:
            a, b, c = np.array([[1, 2, 3], [4, 5, 6]])[::, ::2], np.array([[2], [3]]), 2
            assert np.allclose(f(a, b, c), a * b * c)
        assert (
            capture
            == """
            my_func(x:int=1, y:float=2, z:float=2)
            my_func(x:int=3, y:float=2, z:float=2)
            my_func(x:int=4, y:float=3, z:float=2)
            my_func(x:int=6, y:float=3, z:float=2)
        """
        )
        with capture:
            a, b, c = (
                np.array([[1, 2, 3], [4, 5, 6]], order="F")[::, ::2],
                np.array([[2], [3]]),
                2,
            )
            assert np.allclose(f(a, b, c), a * b * c)
        assert (
            capture
            == """
            my_func(x:int=1, y:float=2, z:float=2)
            my_func(x:int=3, y:float=2, z:float=2)
            my_func(x:int=4, y:float=3, z:float=2)
            my_func(x:int=6, y:float=3, z:float=2)
        """
        )


def test_vectorize():
    assert (numpy.vectorize(
        sin)([1, 2, 3]) == numpy.array([sin(1), sin(2), sin(3)])).all()


def test_vectorize():
    @vectorize(0)
    def vsin(x):
        return sin(x)

    assert vsin([1, x, y]) == [sin(1), sin(x), sin(y)]

    @vectorize(0, 1)
    def vdiff(f, y):
        return diff(f, y)

    assert vdiff([f(x, y, z), g(x, y, z), h(x, y, z)], [x, y, z]) == \
         [[Derivative(f(x, y, z), x), Derivative(f(x, y, z), y),
           Derivative(f(x, y, z), z)], [Derivative(g(x, y, z), x),
                     Derivative(g(x, y, z), y), Derivative(g(x, y, z), z)],
         [Derivative(h(x, y, z), x), Derivative(h(x, y, z), y), Derivative(h(x, y, z), z)]]

