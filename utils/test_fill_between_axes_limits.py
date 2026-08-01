
def test_fill_between_axes_limits():
    fig, ax = plt.subplots()
    x = np.arange(0, 4 * np.pi, 0.01)
    y = 0.1*np.sin(x)
    threshold = 0.075
    ax.plot(x, y, color='black')

    original_lims = (ax.get_xlim(), ax.get_ylim())

    ax.axhline(threshold, color='green', lw=2, alpha=0.7)
    ax.fill_between(x, 0, 1, where=y > threshold,
                    color='green', alpha=0.5, transform=ax.get_xaxis_transform())

    assert (ax.get_xlim(), ax.get_ylim()) == original_lims

