
def test_incompatible_shapes_raise_valueerror():
    # Check that a ValueError is raised for incompatible shapes.

    data = [
        [(3,), (4,)],
        [(2, 3), (2,)],
        [(3,), (3,), (4,)],
        [(1, 3, 4), (2, 3, 3)],
    ]
    for input_shapes in data:
        assert_incompatible_shapes_raise(input_shapes)
        # Reverse the input shapes since broadcasting should be symmetric.
        assert_incompatible_shapes_raise(input_shapes[::-1])

