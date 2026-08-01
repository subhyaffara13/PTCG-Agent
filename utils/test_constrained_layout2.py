
def test_constrained_layout2():
    """Test constrained_layout for 2x2 subplots"""
    fig, axs = plt.subplots(2, 2, layout="constrained")
    for ax in axs.flat:
        example_plot(ax, fontsize=24)

