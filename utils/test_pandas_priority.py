
def test_pandas_priority():
    # GH#48347

    class MyClass:
        __pandas_priority__ = 5000

        def __radd__(self, other):
            return self

    left = MyClass()
    right = Series(range(3))

    assert right.__add__(left) is NotImplemented
    assert right + left is left

