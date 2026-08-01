
def test_inset_colorbar_tight_layout_smoketest():
    fig, ax = plt.subplots(1, 1)
    pts = ax.scatter([0, 1], [0, 1], c=[1, 5])

    cax = inset_axes(ax, width="3%", height="70%")
    plt.colorbar(pts, cax=cax)

    with pytest.warns(UserWarning, match="This figure includes Axes"):
        # Will warn, but not raise an error
        plt.tight_layout()

