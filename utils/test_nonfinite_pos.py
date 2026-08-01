
def test_nonfinite_pos():
    fig, ax = plt.subplots()
    ax.text(0, np.nan, 'nan')
    ax.text(np.inf, 0, 'inf')
    fig.canvas.draw()

