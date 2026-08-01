
def test_removed_axis():
    # Simple smoke test to make sure removing a shared axis works
    fig, axs = plt.subplots(2, sharex=True)
    axs[0].remove()
    fig.canvas.draw()

