
def test_bar_tick_label_multiple():
    # From 2516: plot bar with array of string labels for x axis
    ax = plt.gca()
    ax.bar([1, 2.5], [1, 2], width=[0.2, 0.5], tick_label=['a', 'b'],
           align='center')

