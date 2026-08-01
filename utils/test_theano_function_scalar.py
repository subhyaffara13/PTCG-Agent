
def test_theano_function_scalar():
    """ Test the "scalar" argument to theano_function(). """

    args = [
        ([x, y], [x + y], None, [0]),  # Single 0d output
        ([X, Y], [X + Y], None, [2]),  # Single 2d output
        ([x, y], [x + y], {x: 0, y: 1}, [1]),  # Single 1d output
        ([x, y], [x + y, x - y], None, [0, 0]),  # Two 0d outputs
        ([x, y, X, Y], [x + y, X + Y], None, [0, 2]),  # One 0d output, one 2d
    ]

    # Create and test functions with and without the scalar setting
    for inputs, outputs, in_dims, out_dims in args:
        for scalar in [False, True]:

            f = theano_function_(inputs, outputs, dims=in_dims, scalar=scalar)

            # Check the theano_function attribute is set whether wrapped or not
            assert isinstance(f.theano_function, theano.compile.function_module.Function)

            # Feed in inputs of the appropriate size and get outputs
            in_values = [
                np.ones([1 if bc else 5 for bc in i.type.broadcastable])
                for i in f.theano_function.input_storage
            ]
            out_values = f(*in_values)
            if not isinstance(out_values, list):
                out_values = [out_values]

            # Check output types and shapes
            assert len(out_dims) == len(out_values)
            for d, value in zip(out_dims, out_values):

                if scalar and d == 0:
                    # Should have been converted to a scalar value
                    assert isinstance(value, np.number)

                else:
                    # Otherwise should be an array
                    assert isinstance(value, np.ndarray)
                    assert value.ndim == d

