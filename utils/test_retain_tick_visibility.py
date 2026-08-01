
def test_retain_tick_visibility():
    fig, ax = plt.subplots()
    plt.plot([0, 1, 2], [0, -1, 4])
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.tick_params(axis="y", which="both", length=0)

