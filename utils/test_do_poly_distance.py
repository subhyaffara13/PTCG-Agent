
def test_do_poly_distance():
    # Non-intersecting polygons
    square1 = Polygon (Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0))
    triangle1 = Polygon(Point(1, 2), Point(2, 2), Point(2, 1))
    assert square1._do_poly_distance(triangle1) == sqrt(2)/2

    # Polygons which sides intersect
    square2 = Polygon(Point(1, 0), Point(2, 0), Point(2, 1), Point(1, 1))
    with warns(UserWarning, \
               match="Polygons may intersect producing erroneous output", test_stacklevel=False):
        assert square1._do_poly_distance(square2) == 0

    # Polygons which bodies intersect
    triangle2 = Polygon(Point(0, -1), Point(2, -1), Point(S.Half, S.Half))
    with warns(UserWarning, \
               match="Polygons may intersect producing erroneous output", test_stacklevel=False):
        assert triangle2._do_poly_distance(square1) == 0

