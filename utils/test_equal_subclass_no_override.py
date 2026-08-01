
def test_equal_subclass_no_override(op, dt1, dt2):
    # Test how the three different possible code-paths deal with subclasses

    class MyArr(np.ndarray):
        called_wrap = 0

        def __array_wrap__(self, new, context=None, return_scalar=False):
            type(self).called_wrap += 1
            return super().__array_wrap__(new, context, return_scalar)

    numpy_arr = np.zeros(5, dtype=dt1)
    my_arr = np.zeros(5, dtype=dt2).view(MyArr)

    assert type(op(numpy_arr, my_arr)) is MyArr
    assert type(op(my_arr, numpy_arr)) is MyArr
    # We expect 2 calls (more if there were more fields):
    assert MyArr.called_wrap == 2

