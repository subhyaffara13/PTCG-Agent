
def test_stairs_no_baseline_fill_warns():
    fig, ax = plt.subplots()
    with pytest.warns(UserWarning, match="baseline=None and fill=True"):
        ax.stairs(
            [4, 5, 1, 0, 2],
            [1, 2, 3, 4, 5, 6],
            facecolor="blue",
            baseline=None,
            fill=True
        )

