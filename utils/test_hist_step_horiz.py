
def test_hist_step_horiz():
    # make some data
    d1 = np.linspace(0, 10, 50)
    d2 = np.linspace(1, 3, 20)
    fig, ax = plt.subplots()
    ax.hist((d1, d2), histtype="step", orientation="horizontal")

