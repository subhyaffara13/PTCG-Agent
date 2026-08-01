
def assert_same_as_ufunc(shape0, shape1, transposed=False, flipped=False):
    # Broadcast two shapes against each other and check that the data layout
    # is the same as if a ufunc did the broadcasting.

    x0 = np.zeros(shape0, dtype=int)
    # Note that multiply.reduce's identity element is 1.0, so when shape1==(),
    # this gives the desired n==1.
    n = int(np.multiply.reduce(shape1))
    x1 = np.arange(n).reshape(shape1)
    if transposed:
        x0 = x0.T
        x1 = x1.T
    if flipped:
        x0 = x0[::-1]
        x1 = x1[::-1]
    # Use the add ufunc to do the broadcasting. Since we're adding 0s to x1, the
    # result should be exactly the same as the broadcasted view of x1.
    y = x0 + x1
    b0, b1 = broadcast_arrays(x0, x1)
    assert_array_equal(y, b1)

