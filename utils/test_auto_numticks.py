
def test_auto_numticks():
    axs = plt.figure().subplots(4, 4)
    for ax in axs.flat:  # Tiny, empty subplots have only 3 ticks.
        assert [*ax.get_xticks()] == [*ax.get_yticks()] == [0, 0.5, 1]

