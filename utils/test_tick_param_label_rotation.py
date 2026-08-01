
def test_tick_param_label_rotation():
    fix, (ax, ax2) = plt.subplots(1, 2)
    ax.plot([0, 1], [0, 1])
    ax2.plot([0, 1], [0, 1])
    ax.xaxis.set_tick_params(which='both', rotation=75)
    ax.yaxis.set_tick_params(which='both', rotation=90)
    for text in ax.get_xticklabels(which='both'):
        assert text.get_rotation() == 75
        assert text.get_rotation_mode() == 'default'
    for text in ax.get_yticklabels(which='both'):
        assert text.get_rotation() == 90
        assert text.get_rotation_mode() == 'default'

    ax2.tick_params(axis='x', labelrotation=53, labelrotation_mode='xtick')
    ax2.tick_params(axis='y', rotation=35, rotation_mode='ytick')
    for text in ax2.get_xticklabels(which='major'):
        assert text.get_rotation() == 53
        assert text.get_rotation_mode() == 'xtick'
    for text in ax2.get_yticklabels(which='major'):
        assert text.get_rotation() == 35
        assert text.get_rotation_mode() == 'ytick'

