
def test_init_non_array():
    Rotation((0, 0, 0, 1))
    Rotation([0, 0, 0, 1])
    Rotation([[[0, 0, 0, 1]]])

