
def get_ax():
    """Create a plot and return its Axes."""
    fig, ax = plt.subplots(1, 1)
    ax.plot([0, 200], [0, 200])
    ax.set_aspect(1.0)
    fig.canvas.draw()
    return ax

