
def test_errorbar_mixed_units():
    x = np.arange(10)
    y = [datetime(2020, 5, i * 2 + 1) for i in x]
    fig, ax = plt.subplots()
    ax.errorbar(x, y, timedelta(days=0.5))
    fig.canvas.draw()

