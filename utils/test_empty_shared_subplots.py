
def test_empty_shared_subplots():
    # empty plots with shared axes inherit limits from populated plots
    fig, axs = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
    axs[0].plot([1, 2, 3], [2, 4, 6])
    x0, x1 = axs[1].get_xlim()
    y0, y1 = axs[1].get_ylim()
    assert x0 <= 1
    assert x1 >= 3
    assert y0 <= 2
    assert y1 >= 6

