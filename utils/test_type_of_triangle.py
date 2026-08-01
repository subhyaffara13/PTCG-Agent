
def test_type_of_triangle():
    # Isoceles triangle
    p1 = Polygon(Point(0, 0), Point(5, 0), Point(2, 4))
    assert p1.is_isosceles() == True
    assert p1.is_scalene() == False
    assert p1.is_equilateral() == False

    # Scalene triangle
    p2 = Polygon (Point(0, 0), Point(0, 2), Point(4, 0))
    assert p2.is_isosceles() == False
    assert p2.is_scalene() == True
    assert p2.is_equilateral() == False

    # Equilateral triangle
    p3 = Polygon(Point(0, 0), Point(6, 0), Point(3, sqrt(27)))
    assert p3.is_isosceles() == True
    assert p3.is_scalene() == False
    assert p3.is_equilateral() == True

