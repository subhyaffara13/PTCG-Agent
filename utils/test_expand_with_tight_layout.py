
def test_expand_with_tight_layout():
    # Check issue reported in #10476, and updated due to #10784
    fig, ax = plt.subplots()

    d1 = [1, 2]
    d2 = [2, 1]
    ax.plot(d1, label='series 1')
    ax.plot(d2, label='series 2')
    ax.legend(ncols=2, mode='expand')

    fig.tight_layout()  # where the crash used to happen

