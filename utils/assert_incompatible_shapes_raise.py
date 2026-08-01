
def assert_incompatible_shapes_raise(input_shapes):
    # Broadcast a list of arrays with the given (incompatible) input shapes
    # and check that they raise a ValueError.

    inarrays = [np.zeros(s) for s in input_shapes]
    assert_raises(ValueError, broadcast_arrays, *inarrays)

