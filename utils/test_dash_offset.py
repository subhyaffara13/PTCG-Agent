
def test_dash_offset():
    fig, ax = plt.subplots()
    x = np.linspace(0, 10)
    y = np.ones_like(x)
    for j in range(0, 100, 2):
        ax.plot(x, j*y, ls=(j, (10, 10)), lw=5, color='k')

