
def test_legend_bar():
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    x = np.arange(10)
    b1 = ax.bar(x, x, zdir='y', align='edge', color='m')
    b2 = ax.bar(x, x[::-1], zdir='x', align='edge', color='g')
    ax.legend([b1[0], b2[0]], ['up', 'down'])

