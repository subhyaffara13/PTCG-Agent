
def test_polycollection_close():
    from mpl_toolkits.mplot3d import Axes3D
    plt.rcParams['axes3d.automargin'] = True

    vertsQuad = [
        [[0., 0.], [0., 1.], [1., 1.], [1., 0.]],
        [[0., 1.], [2., 3.], [2., 2.], [1., 1.]],
        [[2., 2.], [2., 3.], [4., 1.], [3., 1.]],
        [[3., 0.], [3., 1.], [4., 1.], [4., 0.]]]

    fig = plt.figure()
    ax = fig.add_axes(Axes3D(fig))

    colors = ['r', 'g', 'b', 'y', 'k']
    zpos = list(range(5))

    poly = mcollections.PolyCollection(
        vertsQuad * len(zpos), linewidth=0.25)
    poly.set_alpha(0.7)

    # need to have a z-value for *each* polygon = element!
    zs = []
    cs = []
    for z, c in zip(zpos, colors):
        zs.extend([z] * len(vertsQuad))
        cs.extend([c] * len(vertsQuad))

    poly.set_color(cs)

    ax.add_collection3d(poly, zs=zs, zdir='y')

    # axis limit settings:
    ax.set_xlim3d(0, 4)
    ax.set_zlim3d(0, 3)
    ax.set_ylim3d(0, 4)

