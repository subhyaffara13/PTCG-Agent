
def test_quadmesh_get_coordinates(pcfunc):
    x = [0, 1, 2]
    y = [2, 4, 6]
    z = np.ones(shape=(2, 2))
    xx, yy = np.meshgrid(x, y)
    coll = getattr(plt, pcfunc)(xx, yy, z)

    # shape (3, 3, 2)
    coords = np.stack([xx.T, yy.T]).T
    assert_array_equal(coll.get_coordinates(), coords)

