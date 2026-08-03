import re

def test_quadmesh_set_array_validation(pcfunc):
    x = np.arange(11)
    y = np.arange(8)
    z = np.random.random((7, 10))
    fig, ax = plt.subplots()
    coll = getattr(ax, pcfunc)(x, y, z)

    with pytest.raises(ValueError, match=re.escape(
            "For X (11) and Y (8) with flat shading, A should have shape "
            "(7, 10, 3) or (7, 10, 4) or (7, 10) or (70,), not (10, 7)")):
        coll.set_array(z.reshape(10, 7))

    z = np.arange(54).reshape((6, 9))
    with pytest.raises(ValueError, match=re.escape(
            "For X (11) and Y (8) with flat shading, A should have shape "
            "(7, 10, 3) or (7, 10, 4) or (7, 10) or (70,), not (6, 9)")):
        coll.set_array(z)
    with pytest.raises(ValueError, match=re.escape(
            "For X (11) and Y (8) with flat shading, A should have shape "
            "(7, 10, 3) or (7, 10, 4) or (7, 10) or (70,), not (54,)")):
        coll.set_array(z.ravel())

    # RGB(A) tests
    z = np.ones((9, 6, 3))  # RGB with wrong X/Y dims
    with pytest.raises(ValueError, match=re.escape(
            "For X (11) and Y (8) with flat shading, A should have shape "
            "(7, 10, 3) or (7, 10, 4) or (7, 10) or (70,), not (9, 6, 3)")):
        coll.set_array(z)

    z = np.ones((9, 6, 4))  # RGBA with wrong X/Y dims
    with pytest.raises(ValueError, match=re.escape(
            "For X (11) and Y (8) with flat shading, A should have shape "
            "(7, 10, 3) or (7, 10, 4) or (7, 10) or (70,), not (9, 6, 4)")):
        coll.set_array(z)

    z = np.ones((7, 10, 2))  # Right X/Y dims, bad 3rd dim
    with pytest.raises(ValueError, match=re.escape(
            "For X (11) and Y (8) with flat shading, A should have shape "
            "(7, 10, 3) or (7, 10, 4) or (7, 10) or (70,), not (7, 10, 2)")):
        coll.set_array(z)

    x = np.arange(10)
    y = np.arange(7)
    z = np.random.random((7, 10))
    fig, ax = plt.subplots()
    coll = ax.pcolormesh(x, y, z, shading='gouraud')

