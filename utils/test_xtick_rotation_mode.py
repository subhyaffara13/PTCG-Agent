
def test_xtick_rotation_mode():
    fig, ax = plt.subplots(figsize=(12, 1))
    ax.set_yticks([])
    ax2 = ax.twiny()

    ax.set_xticks(range(37), ['foo'] * 37, rotation_mode="xtick")
    ax2.set_xticks(range(37), ['foo'] * 37, rotation_mode="xtick")

    angles = np.linspace(0, 360, 37)

    for tick, angle in zip(ax.get_xticklabels(), angles):
        tick.set_rotation(angle)
    for tick, angle in zip(ax2.get_xticklabels(), angles):
        tick.set_rotation(angle)

    plt.subplots_adjust(left=0.01, right=0.99, top=.6, bottom=.4)

