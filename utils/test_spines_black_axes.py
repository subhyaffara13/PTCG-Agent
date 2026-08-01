
def test_spines_black_axes():
    # GitHub #18804
    plt.rcParams["savefig.pad_inches"] = 0
    plt.rcParams["savefig.bbox"] = 'tight'
    fig = plt.figure(0, figsize=(4, 4))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor((0, 0, 0))

