
def test_handlerline3d():
    # Test marker consistency for monolithic Line3D legend handler.
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    ax.scatter([0, 1], [0, 1], marker="v")
    handles = [art3d.Line3D([0], [0], [0], marker="v")]
    leg = ax.legend(handles, ["Aardvark"], numpoints=1)
    assert handles[0].get_marker() == leg.legend_handles[0].get_marker()

