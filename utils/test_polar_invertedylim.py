
def test_polar_invertedylim():
    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.1, 0.8, 0.8), polar=True)
    ax.set_ylim(2, 0)

