
def test_orient_new_methods():
    N = CoordSys3D('N')
    orienter1 = AxisOrienter(q4, N.j)
    orienter2 = SpaceOrienter(q1, q2, q3, '123')
    orienter3 = QuaternionOrienter(q1, q2, q3, q4)
    orienter4 = BodyOrienter(q1, q2, q3, '123')
    D = N.orient_new('D', (orienter1, ))
    E = N.orient_new('E', (orienter2, ))
    F = N.orient_new('F', (orienter3, ))
    G = N.orient_new('G', (orienter4, ))
    assert D == N.orient_new_axis('D', q4, N.j)
    assert E == N.orient_new_space('E', q1, q2, q3, '123')
    assert F == N.orient_new_quaternion('F', q1, q2, q3, q4)
    assert G == N.orient_new_body('G', q1, q2, q3, '123')

