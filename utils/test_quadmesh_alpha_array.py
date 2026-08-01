
def test_quadmesh_alpha_array(pcfunc):
    x = np.arange(4)
    y = np.arange(4)
    z = np.arange(9).reshape((3, 3))
    alpha = z / z.max()
    alpha_flat = alpha.ravel()
    # Provide 2-D alpha:
    fig, (ax0, ax1) = plt.subplots(2)
    coll1 = getattr(ax0, pcfunc)(x, y, z, alpha=alpha)
    coll2 = getattr(ax0, pcfunc)(x, y, z)
    coll2.set_alpha(alpha)
    plt.draw()
    assert_array_equal(coll1.get_facecolors()[:, -1], alpha_flat)
    assert_array_equal(coll2.get_facecolors()[:, -1], alpha_flat)
    # Or provide 1-D alpha:
    fig, (ax0, ax1) = plt.subplots(2)
    coll1 = getattr(ax0, pcfunc)(x, y, z, alpha=alpha)
    coll2 = getattr(ax1, pcfunc)(x, y, z)
    coll2.set_alpha(alpha)
    plt.draw()
    assert_array_equal(coll1.get_facecolors()[:, -1], alpha_flat)
    assert_array_equal(coll2.get_facecolors()[:, -1], alpha_flat)

