
def test_create_new():
    a = CoordSys3D('a')
    c = a.create_new('c', transformation='spherical')
    assert c._parent == a
    assert c.transformation_to_parent() == \
           (c.r*sin(c.theta)*cos(c.phi), c.r*sin(c.theta)*sin(c.phi), c.r*cos(c.theta))
    assert c.transformation_from_parent() == \
           (sqrt(a.x**2 + a.y**2 + a.z**2), acos(a.z/sqrt(a.x**2 + a.y**2 + a.z**2)), atan2(a.y, a.x))

