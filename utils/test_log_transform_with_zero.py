
def test_log_transform_with_zero():
    x = np.arange(-10, 10)
    y = (1.0 - 1.0/(x**2+1))**20

    fig, ax = plt.subplots()
    ax.semilogy(x, y, "-o", lw=15, markeredgecolor='k')
    ax.set_ylim(1e-7, 1)
    ax.grid(True)

