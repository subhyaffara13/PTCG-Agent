
def test_constrained_layout13():
    """Test that padding works."""
    fig, axs = plt.subplots(2, 2, layout="constrained")
    for ax in axs.flat:
        pcm = example_pcolor(ax, fontsize=12)
        fig.colorbar(pcm, ax=ax, shrink=0.6, aspect=20., pad=0.02)
    with pytest.raises(TypeError):
        fig.get_layout_engine().set(wpad=1, hpad=2)
    fig.get_layout_engine().set(w_pad=24./72., h_pad=24./72.)

