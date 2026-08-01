
def test_autoscale_tiny_range():
    # github pull #904
    fig, axs = plt.subplots(2, 2)
    for i, ax in enumerate(axs.flat):
        y1 = 10**(-11 - i)
        ax.plot([0, 1], [1, 1 + y1])

