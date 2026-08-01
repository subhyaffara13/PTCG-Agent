
def test_warn_ignored_scatter_kwargs():
    with pytest.warns(UserWarning,
                      match=r"You passed an edgecolor/edgecolors"):
        plt.scatter([0], [0], marker="+", s=500, facecolor="r", edgecolor="b")

