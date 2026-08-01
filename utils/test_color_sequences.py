
def test_color_sequences():
    # basic access
    assert plt.color_sequences is matplotlib.color_sequences  # same registry
    assert list(plt.color_sequences) == [
        'tab10', 'tab20', 'tab20b', 'tab20c', 'Pastel1', 'Pastel2', 'Paired',
        'Accent', 'okabe_ito', 'Dark2', 'Set1', 'Set2', 'Set3', 'petroff6',
        'petroff8', 'petroff10']
    assert len(plt.color_sequences['tab10']) == 10
    assert len(plt.color_sequences['tab20']) == 20

    tab_colors = [
        'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
        'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    for seq_color, tab_color in zip(plt.color_sequences['tab10'], tab_colors):
        assert mcolors.same_color(seq_color, tab_color)

    # registering
    with pytest.raises(ValueError, match="reserved name"):
        plt.color_sequences.register('tab10', ['r', 'g', 'b'])
    with pytest.raises(ValueError, match="not a valid color specification"):
        plt.color_sequences.register('invalid', ['not a color'])

    rgb_colors = ['r', 'g', 'b']
    plt.color_sequences.register('rgb', rgb_colors)
    assert plt.color_sequences['rgb'] == ['r', 'g', 'b']
    # should not affect the registered sequence because input is copied
    rgb_colors.append('c')
    assert plt.color_sequences['rgb'] == ['r', 'g', 'b']
    # should not affect the registered sequence because returned list is a copy
    plt.color_sequences['rgb'].append('c')
    assert plt.color_sequences['rgb'] == ['r', 'g', 'b']

    # unregister
    plt.color_sequences.unregister('rgb')
    with pytest.raises(KeyError):
        plt.color_sequences['rgb']  # rgb is gone
    plt.color_sequences.unregister('rgb')  # multiple unregisters are ok
    with pytest.raises(ValueError, match="Cannot unregister builtin"):
        plt.color_sequences.unregister('tab10')

