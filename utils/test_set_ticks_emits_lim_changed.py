
def test_set_ticks_emits_lim_changed():
    fig, ax1 = plt.subplots()
    ax1.set_xlim(0.5, 1)
    called_cartesian = []
    ax1.callbacks.connect("xlim_changed", called_cartesian.append)
    ax1.set_xticks([0, 100])
    assert called_cartesian

    fig = plt.figure()
    ax2 = fig.add_subplot(projection="polar")
    ax2.set_ylim(0.5, 1)
    called_polar = []
    ax2.callbacks.connect("ylim_changed", called_polar.append)
    ax2.set_rticks([1, 2, 3])
    assert called_polar

