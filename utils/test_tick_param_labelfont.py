
def test_tick_param_labelfont():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 2, 3, 4])
    ax.set_xlabel('X label in Impact font', fontname='Impact')
    ax.set_ylabel('Y label in xkcd script', fontname='xkcd script')
    ax.tick_params(color='r', labelfontfamily='monospace')
    plt.title('Title in sans-serif')
    for text in ax.get_xticklabels():
        assert text.get_fontfamily()[0] == 'monospace'

