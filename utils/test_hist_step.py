
def test_hist_step():
    # make some data
    d1 = np.linspace(1, 3, 20)
    fig, ax = plt.subplots()
    ax.hist(d1, histtype="step")
    ax.set_ylim(0, 10)
    ax.set_xlim(-1, 5)

