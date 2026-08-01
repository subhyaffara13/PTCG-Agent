
def test_broadcast_to_raises():
    data = [
        [(0,), ()],
        [(1,), ()],
        [(3,), ()],
        [(3,), (1,)],
        [(3,), (2,)],
        [(3,), (4,)],
        [(1, 2), (2, 1)],
        [(1, 1), (1,)],
        [(1,), -1],
        [(1,), (-1,)],
        [(1, 2), (-1, 2)],
    ]
    for orig_shape, target_shape in data:
        arr = np.zeros(orig_shape)
        assert_raises(ValueError, lambda: broadcast_to(arr, target_shape))

