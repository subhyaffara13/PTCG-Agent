
def test_shared_aspect_error():
    fig, axes = plt.subplots(1, 2, sharex=True, sharey=True)
    axes[0].axis("equal")
    with pytest.raises(RuntimeError, match=r"set_aspect\(..., adjustable="):
        fig.draw_without_rendering()

