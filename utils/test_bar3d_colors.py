
def test_bar3d_colors():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for c in ['red', 'green', 'blue', 'yellow']:
        xs = np.arange(len(c))
        ys = np.zeros_like(xs)
        zs = np.zeros_like(ys)
        # Color names with same length as xs/ys/zs should not be split into
        # individual letters.
        ax.bar3d(xs, ys, zs, 1, 1, 1, color=c)

