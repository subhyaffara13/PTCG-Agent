
def test_rigidbody_inertia():
    N = ReferenceFrame('N')
    m, Ix, Iy, Iz, a, b = symbols('m, I_x, I_y, I_z, a, b')
    Io = inertia(N, Ix, Iy, Iz)
    o = Point('o')
    p = o.locatenew('p', a * N.x + b * N.y)
    R = RigidBody('R', o, N, m, (Io, p))
    I_check = inertia(N, Ix - b ** 2 * m, Iy - a ** 2 * m,
                      Iz - m * (a ** 2 + b ** 2), m * a * b)
    assert isinstance(R.inertia, Inertia)
    assert R.inertia == (Io, p)
    assert R.central_inertia == I_check
    R.central_inertia = Io
    assert R.inertia == (Io, o)
    assert R.central_inertia == Io
    R.inertia = (Io, p)
    assert R.inertia == (Io, p)
    assert R.central_inertia == I_check
    # parse Inertia object
    R.inertia = Inertia(Io, o)
    assert R.inertia == (Io, o)

