
def test_poly3dCollection_autoscaling():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    poly = np.array([[0, 0, 0], [1, 1, 3], [1, 0, 4]])
    col = art3d.Poly3DCollection([poly])
    ax.add_collection3d(col)
    assert np.allclose(ax.get_xlim3d(), (-0.020833333333333332, 1.0208333333333333))
    assert np.allclose(ax.get_ylim3d(), (-0.020833333333333332, 1.0208333333333333))
    assert np.allclose(ax.get_zlim3d(), (-0.0833333333333333, 4.083333333333333))

