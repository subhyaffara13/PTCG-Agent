
def test_alpha_rgba():
    # This rcParam would override the explicit setting below, so disable it.
    plt.rcParams['legend.framealpha'] = None
    fig, ax = plt.subplots()
    ax.plot(range(10), lw=5)
    leg = plt.legend(['Longlabel that will go away'], loc='center')
    leg.legendPatch.set_facecolor([1, 0, 0, 0.5])

