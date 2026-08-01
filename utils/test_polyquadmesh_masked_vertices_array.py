
def test_polyquadmesh_masked_vertices_array():
    xx, yy = np.meshgrid([0, 1, 2], [0, 1, 2, 3])
    # 2 x 3 mesh data
    zz = (xx*yy)[:-1, :-1]
    quadmesh = plt.pcolormesh(xx, yy, zz)
    quadmesh.update_scalarmappable()
    quadmesh_fc = quadmesh.get_facecolor()[1:, :]
    # Mask the origin vertex in x
    xx = np.ma.masked_where((xx == 0) & (yy == 0), xx)
    polymesh = plt.pcolor(xx, yy, zz)
    polymesh.update_scalarmappable()
    # One cell should be left out
    assert len(polymesh.get_paths()) == 5
    # Poly version should have the same facecolors as the end of the quadmesh
    assert_array_equal(quadmesh_fc, polymesh.get_facecolor())

    # Mask the origin vertex in y
    yy = np.ma.masked_where((xx == 0) & (yy == 0), yy)
    polymesh = plt.pcolor(xx, yy, zz)
    polymesh.update_scalarmappable()
    # One cell should be left out
    assert len(polymesh.get_paths()) == 5
    # Poly version should have the same facecolors as the end of the quadmesh
    assert_array_equal(quadmesh_fc, polymesh.get_facecolor())

    # Mask the origin cell data
    zz = np.ma.masked_where((xx[:-1, :-1] == 0) & (yy[:-1, :-1] == 0), zz)
    polymesh = plt.pcolor(zz)
    polymesh.update_scalarmappable()
    # One cell should be left out
    assert len(polymesh.get_paths()) == 5
    # Poly version should have the same facecolors as the end of the quadmesh
    assert_array_equal(quadmesh_fc, polymesh.get_facecolor())

    # We should also be able to call set_array with a new mask and get
    # updated polys
    # Remove mask, should add all polys back
    zz = np.arange(6).reshape((3, 2))
    polymesh.set_array(zz)
    polymesh.update_scalarmappable()
    assert len(polymesh.get_paths()) == 6
    # Add mask should remove polys
    zz = np.ma.masked_less(zz, 2)
    polymesh.set_array(zz)
    polymesh.update_scalarmappable()
    assert len(polymesh.get_paths()) == 4

