
def test_function_like():
    # We provide a `__get__` implementation, make sure it works
    assert type(np.mean) is np._core._multiarray_umath._ArrayFunctionDispatcher

    class MyClass:
        def __array__(self, dtype=None, copy=None):
            # valid argument to mean:
            return np.arange(3)

        func1 = staticmethod(np.mean)
        func2 = np.mean
        func3 = classmethod(np.mean)

    m = MyClass()
    assert m.func1([10]) == 10
    assert m.func2() == 1  # mean of the arange
    with pytest.raises(TypeError, match="unsupported operand type"):
        # Tries to operate on the class
        m.func3()

    # Manual binding also works (the above may shortcut):
    bound = np.mean.__get__(m, MyClass)
    assert bound() == 1

    bound = np.mean.__get__(None, MyClass)  # unbound actually
    assert bound([10]) == 10

    bound = np.mean.__get__(MyClass)  # classmethod
    with pytest.raises(TypeError, match="unsupported operand type"):
        bound()

