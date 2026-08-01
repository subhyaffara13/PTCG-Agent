
def test_constrained_layout1():
    """Test constrained_layout for a single subplot"""
    fig = plt.figure(layout="constrained")
    ax = fig.add_subplot()
    example_plot(ax, fontsize=24)

