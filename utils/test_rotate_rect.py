
def test_rotate_rect():
    loc = np.asarray([1.0, 2.0])
    width = 2
    height = 3
    angle = 30.0

    # A rotated rectangle
    rect1 = Rectangle(loc, width, height, angle=angle)

    # A non-rotated rectangle
    rect2 = Rectangle(loc, width, height)

    # Set up an explicit rotation matrix (in radians)
    angle_rad = np.pi * angle / 180.0
    rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                [np.sin(angle_rad),  np.cos(angle_rad)]])

    # Translate to origin, rotate each vertex, and then translate back
    new_verts = np.inner(rotation_matrix, rect2.get_verts() - loc).T + loc

    # They should be the same
    assert_almost_equal(rect1.get_verts(), new_verts)

