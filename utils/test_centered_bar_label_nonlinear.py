
def test_centered_bar_label_nonlinear():
    _, ax = plt.subplots()
    bar_container = ax.barh(['c', 'b', 'a'], [1_000, 5_000, 7_000])
    ax.set_xscale('log')
    ax.set_xlim(1, None)
    ax.bar_label(bar_container, label_type='center')
    ax.set_axis_off()

