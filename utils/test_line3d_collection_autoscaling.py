
def test_line3dCollection_autoscaling():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    lines = [[(0, 0, 0), (1, 4, 2)],
             [(1, 1, 3), (2, 0, 2)],
             [(1, 0, 4), (1, 4, 5)]]

    lc = art3d.Line3DCollection(lines)
    ax.add_collection3d(lc)
    assert np.allclose(ax.get_xlim3d(), (-0.041666666666666664, 2.0416666666666665))
    assert np.allclose(ax.get_ylim3d(), (-0.08333333333333333, 4.083333333333333))
    assert np.allclose(ax.get_zlim3d(), (-0.10416666666666666, 5.104166666666667))

