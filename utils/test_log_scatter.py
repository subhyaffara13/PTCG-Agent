
def test_log_scatter():
    """Issue #1799"""
    fig, ax = plt.subplots(1)

    x = np.arange(10)
    y = np.arange(10) - 1

    ax.scatter(x, y)

    buf = io.BytesIO()
    fig.savefig(buf, format='pdf')

    buf = io.BytesIO()
    fig.savefig(buf, format='eps')

    buf = io.BytesIO()
    fig.savefig(buf, format='svg')

