
def test_broadcast_kwargs():
    # ensure that a TypeError is appropriately raised when
    # np.broadcast_arrays() is called with any keyword
    # argument other than 'subok'
    x = np.arange(10)
    y = np.arange(10)

    with assert_raises_regex(TypeError, 'got an unexpected keyword'):
        broadcast_arrays(x, y, dtype='float64')

