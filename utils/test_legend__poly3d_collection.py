
def test_legend_Poly3dCollection():

    verts = np.asarray([[0, 0, 0], [0, 1, 1], [1, 0, 1]])
    mesh = art3d.Poly3DCollection([verts], label="surface")

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    mesh.set_edgecolor('k')
    handle = ax.add_collection3d(mesh)
    leg = ax.legend()
    assert (leg.legend_handles[0].get_facecolor()
            == handle.get_facecolor()).all()

