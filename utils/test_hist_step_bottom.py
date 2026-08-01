
def test_hist_step_bottom():
    # make some data
    d1 = np.linspace(1, 3, 20)
    fig, ax = plt.subplots()
    ax.hist(d1, bottom=np.arange(10), histtype="stepfilled")

