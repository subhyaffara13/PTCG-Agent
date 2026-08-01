
def test_legend_plot():
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    x = np.arange(10)
    ax.plot(x, 5 - x, 'o', zdir='y', label='z=1')
    ax.plot(x, x - 5, 'o', zdir='y', label='z=-1')
    ax.legend()

