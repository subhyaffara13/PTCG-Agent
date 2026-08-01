
def test_shared_with_aspect_2():
    # Share 2 axes only with 'box':
    fig, axs = plt.subplots(nrows=2, sharex=True, sharey=True)
    axs[0].set_aspect(2, share=True)
    axs[0].plot([1, 2], [3, 4])
    axs[1].plot([3, 4], [1, 2])
    plt.draw()  # Trigger apply_aspect().
    assert axs[0].get_xlim() == axs[1].get_xlim()
    assert axs[0].get_ylim() == axs[1].get_ylim()

