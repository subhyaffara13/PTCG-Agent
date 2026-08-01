
def test_remove_shared_axes_relim():
    fig, ax_lst = plt.subplots(2, 2, sharex='all', sharey='all')
    ax = ax_lst[0][0]
    orig_xlim = ax_lst[0][1].get_xlim()
    ax.remove()
    ax.set_xlim(0, 5)
    assert_array_equal(ax_lst[0][1].get_xlim(), orig_xlim)

