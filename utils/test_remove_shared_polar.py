
def test_remove_shared_polar(fig_ref, fig_test):
    # Removing shared polar axes used to crash.  Test removing them, keeping in
    # both cases just the lower left axes of a grid to avoid running into a
    # separate issue (now being fixed) of ticklabel visibility for shared axes.
    axs = fig_ref.subplots(
        2, 2, sharex=True, subplot_kw={"projection": "polar"})
    for i in [0, 1, 3]:
        axs.flat[i].remove()
    axs = fig_test.subplots(
        2, 2, sharey=True, subplot_kw={"projection": "polar"})
    for i in [0, 1, 3]:
        axs.flat[i].remove()

