
def test_handlerline2d():
    # Test marker consistency for monolithic Line2D legend handler (#11357).
    fig, ax = plt.subplots()
    ax.scatter([0, 1], [0, 1], marker="v")
    handles = [mlines.Line2D([0], [0], marker="v")]
    leg = ax.legend(handles, ["Aardvark"], numpoints=1)
    assert handles[0].get_marker() == leg.legend_handles[0].get_marker()

