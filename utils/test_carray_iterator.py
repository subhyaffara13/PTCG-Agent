
def test_carray_iterator():
    """#4100: Check for proper iterator overload with C-Arrays"""
    args_gt = [float(i) for i in range(3)]
    arr_h = m.CArrayHolder(*args_gt)
    args = list(arr_h)
    assert args_gt == args

