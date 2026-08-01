
def assert_shapes_correct(input_shapes, expected_shape):
    # Broadcast a list of arrays with the given input shapes and check the
    # common output shape.

    inarrays = [np.zeros(s) for s in input_shapes]
    outarrays = broadcast_arrays(*inarrays)
    outshapes = [a.shape for a in outarrays]
    expected = [expected_shape] * len(inarrays)
    assert_equal(outshapes, expected)

