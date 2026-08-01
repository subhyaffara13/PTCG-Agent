
def test_pathpatch_3d(fig_test, fig_ref):
    ax = fig_ref.add_subplot(projection="3d")
    path = Path.unit_rectangle()
    patch = PathPatch(path)
    art3d.pathpatch_2d_to_3d(patch, z=(0, 0.5, 0.7, 1, 0), zdir='y')
    ax.add_artist(patch)

    ax = fig_test.add_subplot(projection="3d")
    pp3d = art3d.PathPatch3D(path, zs=(0, 0.5, 0.7, 1, 0), zdir='y')
    ax.add_artist(pp3d)

