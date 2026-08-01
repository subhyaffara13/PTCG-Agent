
def test_ytick_rotation_mode():
    fig, ax = plt.subplots(figsize=(1, 12))
    ax.set_xticks([])
    ax2 = ax.twinx()

    ax.set_yticks(range(37), ['foo'] * 37, rotation_mode="ytick")
    ax2.set_yticks(range(37), ['foo'] * 37, rotation_mode='ytick')

    angles = np.linspace(0, 360, 37)
    for tick, angle in zip(ax.get_yticklabels(), angles):
        tick.set_rotation(angle)
    for tick, angle in zip(ax2.get_yticklabels(), angles):
        tick.set_rotation(angle)

    plt.subplots_adjust(left=0.4, right=0.6, top=.99, bottom=.01)

