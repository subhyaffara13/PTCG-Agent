
def test_auto_vel_multiple_path_warning_msg():
    N = ReferenceFrame('N')
    O = Point('O')
    P = Point('P')
    Q = Point('Q')
    P.set_vel(N, N.x)
    Q.set_vel(N, N.y)
    O.set_pos(P, N.z)
    O.set_pos(Q, N.y)
    with warnings.catch_warnings(record = True) as w: #There are two possible paths in this point tree, thus a warning is raised
        warnings.simplefilter("always")
        O.vel(N)
        msg = str(w[-1].message).replace("\n", " ")
        assert issubclass(w[-1].category, UserWarning)
        assert 'Velocity' in msg
        assert 'automatically calculated based on point' in msg
        assert 'Velocities from these points are not necessarily the same. This may cause errors in your calculations.' in msg

