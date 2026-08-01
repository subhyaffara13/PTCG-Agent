
def test_same_input_shapes():
    # Check that the final shape is just the input shape.

    data = [
        (),
        (1,),
        (3,),
        (0, 1),
        (0, 3),
        (1, 0),
        (3, 0),
        (1, 3),
        (3, 1),
        (3, 3),
    ]
    for shape in data:
        input_shapes = [shape]
        # Single input.
        assert_shapes_correct(input_shapes, shape)
        # Double input.
        input_shapes2 = [shape, shape]
        assert_shapes_correct(input_shapes2, shape)
        # Triple input.
        input_shapes3 = [shape, shape, shape]
        assert_shapes_correct(input_shapes3, shape)

