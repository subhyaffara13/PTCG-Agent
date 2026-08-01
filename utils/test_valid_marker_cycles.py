
def test_valid_marker_cycles():
    fig, ax = plt.subplots()
    ax.set_prop_cycle(cycler(marker=[1, "+", ".", 4]))

