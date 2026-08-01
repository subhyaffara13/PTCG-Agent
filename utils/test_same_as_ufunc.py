
def test_same_as_ufunc():
    # Check that the data layout is the same as if a ufunc did the operation.

    data = [
        [[(1,), (3,)], (3,)],
        [[(1, 3), (3, 3)], (3, 3)],
        [[(3, 1), (3, 3)], (3, 3)],
        [[(1, 3), (3, 1)], (3, 3)],
        [[(1, 1), (3, 3)], (3, 3)],
        [[(1, 1), (1, 3)], (1, 3)],
        [[(1, 1), (3, 1)], (3, 1)],
        [[(1, 0), (0, 0)], (0, 0)],
        [[(0, 1), (0, 0)], (0, 0)],
        [[(1, 0), (0, 1)], (0, 0)],
        [[(1, 1), (0, 0)], (0, 0)],
        [[(1, 1), (1, 0)], (1, 0)],
        [[(1, 1), (0, 1)], (0, 1)],
        [[(), (3,)], (3,)],
        [[(3,), (3, 3)], (3, 3)],
        [[(3,), (3, 1)], (3, 3)],
        [[(1,), (3, 3)], (3, 3)],
        [[(), (3, 3)], (3, 3)],
        [[(1, 1), (3,)], (1, 3)],
        [[(1,), (3, 1)], (3, 1)],
        [[(1,), (1, 3)], (1, 3)],
        [[(), (1, 3)], (1, 3)],
        [[(), (3, 1)], (3, 1)],
        [[(), (0,)], (0,)],
        [[(0,), (0, 0)], (0, 0)],
        [[(0,), (0, 1)], (0, 0)],
        [[(1,), (0, 0)], (0, 0)],
        [[(), (0, 0)], (0, 0)],
        [[(1, 1), (0,)], (1, 0)],
        [[(1,), (0, 1)], (0, 1)],
        [[(1,), (1, 0)], (1, 0)],
        [[(), (1, 0)], (1, 0)],
        [[(), (0, 1)], (0, 1)],
    ]
    for input_shapes, expected_shape in data:
        assert_same_as_ufunc(input_shapes[0], input_shapes[1],
                             f"Shapes: {input_shapes[0]} {input_shapes[1]}")
        # Reverse the input shapes since broadcasting should be symmetric.
        assert_same_as_ufunc(input_shapes[1], input_shapes[0])
        # Try them transposed, too.
        assert_same_as_ufunc(input_shapes[0], input_shapes[1], True)
        # ... and flipped for non-rank-0 inputs in order to test negative
        # strides.
        if () not in input_shapes:
            assert_same_as_ufunc(input_shapes[0], input_shapes[1], False, True)
            assert_same_as_ufunc(input_shapes[0], input_shapes[1], True, True)

