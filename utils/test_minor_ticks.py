
def test_minor_ticks():
    ax = plt.figure().add_subplot(projection="3d")
    ax.set_xticks([0.25], minor=True)
    ax.set_xticklabels(["quarter"], minor=True)
    ax.set_yticks([0.33], minor=True)
    ax.set_yticklabels(["third"], minor=True)
    ax.set_zticks([0.50], minor=True)
    ax.set_zticklabels(["half"], minor=True)


def test_minor_ticks():
    plt.figure()
    plt.plot(np.arange(1, 10))
    tick_pos, tick_labels = plt.xticks(minor=True)
    assert np.all(tick_labels == np.array([], dtype=np.float64))
    assert tick_labels == []

    plt.yticks(ticks=[3.5, 6.5], labels=["a", "b"], minor=True)
    ax = plt.gca()
    tick_pos = ax.get_yticks(minor=True)
    tick_labels = ax.get_yticklabels(minor=True)
    assert np.all(tick_pos == np.array([3.5, 6.5]))
    assert [l.get_text() for l in tick_labels] == ['a', 'b']

