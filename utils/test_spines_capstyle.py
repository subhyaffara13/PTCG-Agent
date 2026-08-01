
def test_spines_capstyle():
    # issue 2542
    plt.rc('axes', linewidth=20)
    fig, ax = plt.subplots()
    ax.set_xticks([])
    ax.set_yticks([])

