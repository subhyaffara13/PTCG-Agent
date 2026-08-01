
def test_Poly3DCollection_get_path():
    # Smoke test to see that get_path does not raise
    # See GH#27361
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    p = Circle((0, 0), 1.0)
    ax.add_patch(p)
    art3d.pathpatch_2d_to_3d(p)
    p.get_path()

