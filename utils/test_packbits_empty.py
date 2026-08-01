
def test_packbits_empty():
    shapes = [
        (0,), (10, 20, 0), (10, 0, 20), (0, 10, 20), (20, 0, 0), (0, 20, 0),
        (0, 0, 20), (0, 0, 0),
    ]
    for dt in '?bBhHiIlLqQ':
        for shape in shapes:
            a = np.empty(shape, dtype=dt)
            b = np.packbits(a)
            assert_equal(b.dtype, np.uint8)
            assert_equal(b.shape, (0,))

