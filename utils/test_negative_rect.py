
def test_negative_rect():
    # These two rectangles have the same vertices, but starting from a
    # different point.  (We also drop the last vertex, which is a duplicate.)
    pos_vertices = Rectangle((-3, -2), 3, 2).get_verts()[:-1]
    neg_vertices = Rectangle((0, 0), -3, -2).get_verts()[:-1]
    assert_array_equal(np.roll(neg_vertices, 2, 0), pos_vertices)

