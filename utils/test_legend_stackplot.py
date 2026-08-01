
def test_legend_stackplot():
    """Test legend for PolyCollection using stackplot."""
    # related to #1341, #1943, and PR #3303
    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 10)
    y1 = 1.0 * x
    y2 = 2.0 * x + 1
    y3 = 3.0 * x + 2
    ax.stackplot(x, y1, y2, y3, labels=['y1', 'y2', 'y3'])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 70)
    ax.legend(loc='best')

