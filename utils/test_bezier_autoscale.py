
def test_bezier_autoscale():
    # Check that bezier curves autoscale to their curves, and not their
    # control points
    verts = [[-1, 0],
             [0, -1],
             [1, 0],
             [1, 0]]
    codes = [mpath.Path.MOVETO,
             mpath.Path.CURVE3,
             mpath.Path.CURVE3,
             mpath.Path.CLOSEPOLY]
    p = mpath.Path(verts, codes)

    fig, ax = plt.subplots()
    ax.add_patch(mpatches.PathPatch(p))
    ax.autoscale()
    # Bottom ylim should be at the edge of the curve (-0.5), and not include
    # the control point (at -1)
    assert ax.get_ylim()[0] == -0.5

