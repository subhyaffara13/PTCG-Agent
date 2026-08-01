
def test_set_ticks_inverted():
    fig, ax = plt.subplots()
    ax.invert_xaxis()
    ax.set_xticks([.3, .7])
    assert ax.get_xlim() == (1, 0)
    ax.set_xticks([-1])
    assert ax.get_xlim() == (1, -1)

