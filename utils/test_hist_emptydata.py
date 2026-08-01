
def test_hist_emptydata():
    fig, ax = plt.subplots()
    ax.hist([[], range(10), range(10)], histtype="step")

