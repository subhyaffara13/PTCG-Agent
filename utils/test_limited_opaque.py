
def test_limited_opaque(install_temp):
    import limited_api_opaque

    import numpy as np
    arr = np.ones((200, 200))
    assert limited_api_opaque.nonzero(arr) == 200 * 200

    # Test PyArray_ITER_NEXT / PyArray_ITER_DATA / PyArray_ITER_NOTDONE
    arr = np.arange(12.0).reshape(3, 4)
    assert limited_api_opaque.iter_next(arr) == 66.0

    # Test PyArray_ITER_GOTO1D
    assert limited_api_opaque.iter_goto1d(arr, 5) == 5.0
    assert limited_api_opaque.iter_goto1d(arr, -1) == 11.0

    # Test PyArray_ITER_RESET
    assert limited_api_opaque.iter_reset(arr) == 66.0

    # Test PyArray_MultiIter_NEXT / RESET / DATA with broadcasting
    a = np.arange(3.0).reshape(3, 1)   # shape (3, 1)
    b = np.arange(4.0).reshape(1, 4)   # shape (1, 4)
    # Each broadcast element is a[i] + b[j], total sum:
    expected = float(np.sum(a + b))
    assert limited_api_opaque.multi_iter_next(a, b) == expected

    # Test PyArray_ITER_GOTO
    arr = np.arange(12.0).reshape(3, 4)
    assert limited_api_opaque.iter_goto(arr, (1, 2)) == 6.0
    assert limited_api_opaque.iter_goto(arr, (2, 3)) == 11.0

    # Test PyArray_MultiIter_GOTO
    a = np.arange(3.0).reshape(3, 1)
    b = np.arange(4.0).reshape(1, 4)
    va, vb = limited_api_opaque.multi_iter_goto(a, b, (1, 2))
    assert va == 1.0 and vb == 2.0

    # Test PyArray_MultiIter_GOTO1D
    # flat index 6 in (3,4) broadcast → row 1, col 2
    va, vb = limited_api_opaque.multi_iter_goto1d(a, b, 6)
    assert va == 1.0 and vb == 2.0

    # Test PyArray_MultiIter_NEXTi
    a = np.arange(6.0).reshape(2, 3)
    b = np.zeros((2, 3))
    # Advance iter 0 by 3 steps → flat index 3 → value 3.0
    assert limited_api_opaque.multi_iter_nexti(a, b, 3) == 3.0

