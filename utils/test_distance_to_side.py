
def test_distance_to_side():
    point = (0, 0, 0)
    assert distance_to_side(point, [(0, 0, 1), (0, 1, 0)], (1, 0, 0)) == -sqrt(2)/2

