
def test_is_vertex():
    assert is_vertex(2) is False
    assert is_vertex((2, 3)) is True
    assert is_vertex(Point(2, 3)) is True
    assert is_vertex((2, 3, 4)) is True
    assert is_vertex((2, 3, 4, 5)) is False

