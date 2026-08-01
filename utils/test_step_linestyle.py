
def test_step_linestyle():
    # Tolerance caused by reordering of floating-point operations
    # Remove when regenerating the images
    x = y = np.arange(10)

    # First illustrate basic pyplot interface, using defaults where possible.
    fig, ax_lst = plt.subplots(2, 2)
    ax_lst = ax_lst.flatten()

    ln_styles = ['-', '--', '-.', ':']

    for ax, ls in zip(ax_lst, ln_styles):
        ax.step(x, y, lw=5, linestyle=ls, where='pre')
        ax.step(x, y + 1, lw=5, linestyle=ls, where='mid')
        ax.step(x, y + 2, lw=5, linestyle=ls, where='post')
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 7)

    # Reuse testcase from above for a labeled data test
    data = {"X": x, "Y0": y, "Y1": y+1, "Y2": y+2}
    fig, ax_lst = plt.subplots(2, 2)
    ax_lst = ax_lst.flatten()
    ln_styles = ['-', '--', '-.', ':']
    for ax, ls in zip(ax_lst, ln_styles):
        ax.step("X", "Y0", lw=5, linestyle=ls, where='pre', data=data)
        ax.step("X", "Y1", lw=5, linestyle=ls, where='mid', data=data)
        ax.step("X", "Y2", lw=5, linestyle=ls, where='post', data=data)
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 7)

