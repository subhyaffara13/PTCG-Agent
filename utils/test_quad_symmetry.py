
def test_quad_symmetry():
    assert quadts(sin, [-1, 1]) == 0
    assert quadgl(sin, [-1, 1]) == 0

