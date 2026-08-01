
def test_xylim_changed_shared():
    fig, axs = plt.subplots(2, sharex=True, sharey=True)
    events = []
    axs[1].callbacks.connect("xlim_changed", events.append)
    axs[1].callbacks.connect("ylim_changed", events.append)
    axs[0].set(xlim=[1, 3], ylim=[2, 4])
    assert events == [axs[1], axs[1]]

