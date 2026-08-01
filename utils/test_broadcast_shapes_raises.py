
def test_broadcast_shapes_raises():
    # tests public broadcast_shapes
    data = [
        [(3,), (4,)],
        [(2, 3), (2,)],
        [(3,), (3,), (4,)],
        [(1, 3, 4), (2, 3, 3)],
        [(1, 2), (3, 1), (3, 2), (10, 5)],
        [2, (2, 3)],
    ]
    for input_shapes in data:
        assert_raises(ValueError, lambda: broadcast_shapes(*input_shapes))

    bad_args = [(2,)] * 32 + [(3,)] * 32
    assert_raises(ValueError, lambda: broadcast_shapes(*bad_args))

