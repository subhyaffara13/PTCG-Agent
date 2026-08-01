
def test_text_labelsize():
    """
    tests for issue #1172
    """
    fig = plt.figure()
    ax = fig.gca()
    ax.tick_params(labelsize='large')
    ax.tick_params(direction='out')

