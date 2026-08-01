
def test_centered_bar_label_label_beyond_limits():
    fig, ax = plt.subplots()

    last = 0
    for label, value in zip(['a', 'b', 'c'], [10, 20, 50]):
        bar_container = ax.barh('col', value, label=label, left=last)
        ax.bar_label(bar_container, label_type='center')
        last += value
    ax.set_xlim(None, 20)

    fig.draw_without_rendering()

